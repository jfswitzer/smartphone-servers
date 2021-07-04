import pandas as pd
import matplotlib.pyplot as plt
FONTSIZE = '16'
df = pd.read_csv('geekbenches.csv')
blues = df[df['source']=='us']
xb = blues['Year']
yb = blues['GeekBench single core']
nb = blues['Model']

fig, ax = plt.subplots()
ax.scatter(xb,yb,s=180,color='darkblue',label='Benchmarked by us',marker='v')
for i, txt in enumerate(nb):
    ax.annotate('  '+txt, (xb[i], yb[i]),fontsize=12,xytext=(0,-8.5),textcoords='offset points')

yellows = df[df['source']=='them']
xy = yellows['Year']
yy = yellows['GeekBench single core']
ny = yellows['Model']
ax.scatter(xy,yy,s=180,color='darkorange',label='GeekBench mean',marker='d')
for row in yellows.iterrows():
    row = row[1]
    ax.annotate('  '+row['Model'], (row['Year'], row['GeekBench single core']),fontsize=12,xytext=(0,-8.5),textcoords='offset points')
ax.annotate('Intel Core i3-8100',(2012,1005),style='italic',fontsize=FONTSIZE)
plt.axhline(y = 1000, color = 'black', linestyle = '--')
plt.xlim([2011,2023])
plt.xlabel('Release Year',fontsize=FONTSIZE)
plt.ylabel('GeekBench Single Core Score',fontsize=FONTSIZE)
plt.xticks([2012,2014,2016,2018,2020,2022],fontsize=FONTSIZE)
plt.yticks(fontsize=FONTSIZE)
fig.tight_layout()
fig.set_size_inches(10.5, 7.5)
plt.legend(fontsize=FONTSIZE,loc=(0.02,0.76))
fig.savefig('results.eps', dpi=100)
plt.show()
