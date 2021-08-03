with open('pstat.out','r') as f:
    with open('cleaned.csv','a') as g:
        for line in f.readlines():
            if not 'Time' in line:
                g.write(line)
