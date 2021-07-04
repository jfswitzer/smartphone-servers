import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import numpy as NP
import glob
import os
import sys

def main():
    #caiso
    li = []
    path = "caiso_2019"
    all_files = glob.glob(os.path.join(path, "*2019*.csv"))
    
    t = pd.DataFrame({})
    for filename in all_files:
        t = pd.read_csv(filename, index_col=None, header=0)
        li.append(t)
    df = pd.concat(li, axis=0, ignore_index=True)    
    #only get lmps
    df = df[df["LMP_TYPE"]=="LMP"]
    from datetime import datetime
    #have to see if this works or not
    df["HOUR"] = df["INTERVALSTARTTIME_GMT"].map(lambda s: int(datetime.strptime(s,'%Y-%m-%dT%H:%M:00-00:00').hour-8))
    df["HOUR"] = df["HOUR"].map(lambda x: x+24 if x<0 else x)    
    prices = df.groupby("HOUR").mean()
    normalized_prices=(prices-prices.mean())/prices.std()
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(normalized_prices.index, normalized_prices['VALUE'], label="Mean Energy Price (Normalized)", color="grey")    
    ax.yaxis.set_ticks([])
    plt.axhline(0, color='black', linewidth=1)
    plt.xlabel("Time of Day")
    def timstr(i,y):
        i = int(i)
        s = 'AM'
        if i >= 12:
            s = 'PM'
        h = i % 12
        return str(h)+s
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(timstr))
    plt.ylim(-4,4)
    plt.legend()
    plt.savefig('output.png')
        
if __name__ == "__main__":
    main()

