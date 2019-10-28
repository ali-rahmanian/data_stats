import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
cd={}
entries=os.listdir('data/Milano_WeatherPhenomena')
outlier_num=np.zeros(len(entries))
for i,entry in enumerate(entries):
    entries[i]=entries[i][9:-4]
    cd[i]=pd.read_csv('data/Milano_WeatherPhenomena/mi_meteo_'+entries[i]+'.csv', usecols=[1,2],names=['time','val'], converters= {'time': pd.to_datetime})
    q1=cd[i]['val'].quantile(0.25)
    q3=cd[i]['val'].quantile(0.75)
    iqr=q3-q1
    for value in cd[i]['val']:
        if(value<(q1-1.5*iqr) or (value>q3+1.5*iqr)):
            outlier_num[i]+=1
plt.bar(range(len(entries)), outlier_num, align='center', alpha=0.5)
plt.xticks(range(len(entries)), entries, fontsize=12, rotation=90)
plt.ylabel('Number of outliers')
plt.xlabel('Sensor ID')
plt.title('Outliers in different datasets', y=1.08)
plt.show()