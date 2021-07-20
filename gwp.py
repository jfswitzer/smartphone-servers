import matplotlib.pyplot as plt
import numpy as np

FONTSIZE=12
#e = 0.6029
# def gwp(y,u):
#     return (P+(u+0.5)*8.760*y*e)/(3+y)
# yr = np.linspace(0,5,1000)

# gwp20 = [gwp(y,0.2) for y in yr]
# gwp50 = [gwp(y,0.5) for y in yr]
# gwp100 = [gwp(y,1) for y in yr]

# fig, ax = plt.subplots()
# ax.plot(yr,gwp20,label="20% Utilization")
# ax.plot(yr,gwp50,label="50% Utilization")
# ax.plot(yr,gwp100,label="100% Utilization")
# plt.xlabel("Years of Reuse",fontsize=FONTSIZE)
# plt.ylabel("Yearly GWP ($kgCO_{2}e$/year)",fontsize=FONTSIZE)
# ax.annotate('100%',(4.4,11.55),style='italic')
# ax.annotate('50%',(4.4,10),style='italic')
# ax.annotate('20%',(4.4,9),style='italic')
# plt.xlim(0,5)
# plt.xticks(fontsize=11)
# plt.yticks(fontsize=11)
# fig.tight_layout()
# fig.set_size_inches(5, 3.5)
# fig.savefig('gwp.eps', dpi=100)
# plt.show()

P = 43.31+7
def gwp(y,e):
    return (P+1.92*8.760*y*e)/(3+y)
yr = np.linspace(0,5,1000)

gwp_solar = [gwp(y,0.048) for y in yr]
gwp_gas = [gwp(y,0.49) for y in yr]
gwp_world = [gwp(y,0.6029) for y in yr]
gwp_ca = [gwp(y,0.2567) for y in yr]

fig, ax = plt.subplots()
ax.plot(yr,gwp_world,label="World Electricity Mix",linewidth=2)
#ax.plot(yr,gwp_gas,label="Natural Gas",linewidth=2)
ax.plot(yr,gwp_ca,label="CA Eletricity Mix",linewidth=2)
ax.plot(yr,gwp_solar,label="Solar",linewidth=2)
p100 = P/3
plt.hlines(p100,0,5,linestyles="dashed",colors=["lightgrey"])
ax.annotate('Baseline',(4.25,p100-0.6),style='italic',color="grey")
p75 = 0.75*(P/3)
plt.hlines(p75,0,5,linestyles="dashed",colors=["lightgrey"])
ax.annotate('$-$25%',(4.45,p75-0.6),style='italic',color="grey")
p50 = 0.5*(P/3)
plt.hlines(p50,0,5,linestyles="dashed",colors=["lightgrey"])
ax.annotate('$-$50%',(4.45,p50-0.6),style='italic',color="grey")

plt.xlabel("Years of Reuse",fontsize=FONTSIZE+1)
plt.ylabel(r'Carbon Intensity $\frac{kgCO_{2}e}{year}$',fontsize=FONTSIZE+1)
plt.legend(loc='lower left')
plt.xlim(0,5)
plt.ylim(6,P/3+1)
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)
fig.tight_layout()
fig.set_size_inches(5, 3.5)
fig.savefig('gwp.eps', dpi=100)
plt.show()
