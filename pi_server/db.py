from peewee import *
from playhouse.sqlite_ext import *
import datetime, power

db = SqliteDatabase('database.db')

# number of minutes in between heart beats that still considers the device is alive and healthy
HEARTBEAT_ACTIVE_RANGE_MINUTES = 1
METADATA_HISTORY_SIZE = 5
MAX_JOB_ATTEMPTS = 5

class BaseModel(Model):
    class Meta:
        database = db

class Device(BaseModel):
    id = IntegerField(primary_key=True, unique=True, null=False)

    metadata = JSONField()

    # This will store the last `METADATA_HISTORY_SIZE` metadatas received from the device
    # NEVER set this field value manually, this will be auto-handled in update_metadata_history(),
    # which should be called whenever the device's metadata field has been updated
    metadata_history = JSONField()

    smart_plug_key = TextField()

    time_created = DateTimeField(default=datetime.datetime.utcnow)
    last_heartbeat = DateTimeField(default=datetime.datetime.utcnow)
    time_updated = DateTimeField()

    @property
    def is_active(self):
        if not self.last_heartbeat:
            return False
        return datetime.datetime.utcnow() - self.last_heartbeat <= datetime.timedelta(minutes=HEARTBEAT_ACTIVE_RANGE_MINUTES)

    def update_metadata_history(self):
        metadata_history = self.metadata_history
        metadata_history.append(self.metadata)
        metadata_history = metadata_history[-METADATA_HISTORY_SIZE:]
        self.metadata_history = metadata_history

    def get_avg_historical_system_metric(self, metric_name, default_value=0):
        vals = [metadata.get("system", {}).get(metric_name, default_value) for metadata in self.metadata_history]
        return sum(vals) / len(vals)

    def save(self, *args, **kwargs):
        self.time_updated = datetime.datetime.utcnow()
        return super(Device, self).save(*args, **kwargs)

    def to_json(self):
        return {
            "id" : self.id,
            "last_heartbeat" : str(self.last_heartbeat),
            "time_created" : str(self.time_created),
            "time_updated" : str(self.time_updated),
            "assigned_jobs" : {
                "num_total" : len(self.assigned_jobs)
            },
            "smart_plug_key" : self.smart_plug_key,
            "metadata" : self.metadata
        }

    def stop_charging(self):
        power.power_off(self.smart_plug_key)

    def start_charging(self):
        power.power_on(self.smart_plug_key)

    def get_battery_level(self):
        return self.metadata['system']['battery']

    def needs_to_start_charging(self):
        return self.get_battery_level() < 0.2

    def needs_to_stop_charging(self):
        return self.get_battery_level() > 0.8


class Job(BaseModel):
    UNASSIGNED = 0
    ASSIGNED = 1
    FAILED = 2
    SUCCEEDED = 3

    num_attempts = IntegerField(default=0)

    status = IntegerField(choices=[(UNASSIGNED, "UNASSIGNED"), (ASSIGNED, "ASSIGNED"), (FAILED, "FAILED"), (SUCCEEDED, "SUCCESS")], default=0)
    assigned_device = ForeignKeyField(Device, backref="assigned_jobs", null=True, default=None)

    # Resource limits
    # -1 means no limit
    cpus = IntegerField(default=-1)
    memory_mb = IntegerField(default=-1)
    max_runtime_secs = IntegerField(default=-1)

    # Specification
    code_url = TextField()

    time_created = DateTimeField(default=datetime.datetime.utcnow)
    time_updated = DateTimeField()

    def save(self, *args, **kwargs):
        self.time_updated = datetime.datetime.utcnow()
        return super(Job, self).save(*args, **kwargs)

    @property
    def can_be_retried(self):
        if self.status == Job.SUCCEEDED:
            return False
        return self.num_attempts < MAX_JOB_ATTEMPTS

    def cancel(self):
        if self.assigned_device:
            from app import socketio
            target_device_id = self.assigned_device.id
            socketio.emit("cancel_job", {'device_id': target_device_id, 'job_id': self.id})

    def to_json(self):
        return {
            "id" : self.id,
            "status" : self.status,
            "num_attempts" : self.num_attempts,
            "can_be_retried" : self.can_be_retried,
            "assigned_device_id" : None if not self.assigned_device else self.assigned_device.id,
            "resource_requirements" : {
                "cpus" : self.cpus,
                "memory_mb" : self.memory_mb,
                "max_runtime_secs" : self.max_runtime_secs
            },
            "code_url" : self.code_url,
            "time_created" : str(self.time_created),
            "time_updated" : str(self.time_updated)
        }


def create_device(device_id, smart_plug_key, metadata):
    device = Device(id=device_id, smart_plug_key=smart_plug_key, metadata=metadata)
    device.update_metadata_history()
    device.save()

def create_job(job_spec):
    assert "resource_requirements" in job_spec and "code_url" in job_spec
    job = Job(status=Job.UNASSIGNED,
              cpus=job_spec["resource_requirements"].get("cpus", -1),
              memory_mb=job_spec["resource_requirements"].get("memory_mb", -1),
              max_runtime_secs=job_spec["resource_requirements"].get("max_runtime_secs", -1),
              code_url = job_spec['code_url'])
    job.save()
    return job

def get_device(device_id):
    try:
        return Device.get(Device.id == device_id)
    except:
        return None

def get_devices_not_currently_in_use():
    # TODO: A more optimized query would involve JOINS, but for now, we're doing it the naive way
    return [device for device in get_all_devices() if len(device.assigned_jobs) == 0]

def get_target_device_for_job():
    # Choose a device id that currently doesn't have any assigned jobs
    # TODO: This logic would of course change once we begin to account for cpus/mem, at which point,
    #  the device selection query would select all devices that have enough resources to run this job, etc.
    candidate_devices_for_job = get_devices_not_currently_in_use()
    candidate_devices_for_job = [device for device in candidate_devices_for_job if device.is_active]
    candidate_devices_for_job = sorted(candidate_devices_for_job, key = lambda device: device.get_avg_historical_system_metric(metric_name="cpu"))
    if not candidate_devices_for_job:
        return None
    # Pick the device that's available, healthy, and has the lowest historical avg. cpu usage
    return candidate_devices_for_job[0]

def schedule_job(job):
    from app import socketio

    # Choose a device to send this job to
    # TODO: Add some sort of cron/redundancy to attempt to re-assign jobs that don't get acknowledged, etc.
    #  This should occur as some sort of cron process, but for the sake of an MVP, we just try to assign each job once
    target_device = get_target_device_for_job()

    if not target_device:
        return False

    socketio.emit("task_submission", {'device_id': target_device.id, 'job': job.to_json()})
    return True

def get_all_devices():
    return list(Device.select())

def get_all_jobs():
    return list(Job.select())

def get_job(job_id):
    try:
        return Job.get(Job.id == job_id)
    except:
        return None

def update_device(device_id, metadata):
    device = get_device(device_id=device_id)
    device.metadata = metadata
    device.update_metadata_history()
    device.save()

def update_job(job_id, status):
    job = get_job(job_id=job_id)
    job.status = status
    return job