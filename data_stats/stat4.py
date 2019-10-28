import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
cd={}
entries=['14121','2006','5908','9341']
cd[0]=pd.read_csv('data/Milano_WeatherPhenomena/mi_meteo_14121.csv', usecols=[1,2],names=['time','val'], converters= {'time': pd.to_datetime})
cd[1]=pd.read_csv('data/Milano_WeatherPhenomena/mi_meteo_2006.csv', usecols=[1,2],names=['time','val'], converters= {'time': pd.to_datetime})
cd[2]=pd.read_csv('data/Milano_WeatherPhenomena/mi_meteo_5908.csv', usecols=[1,2],names=['time','val'], converters= {'time': pd.to_datetime})
cd[3]=pd.read_csv('data/Milano_WeatherPhenomena/mi_meteo_9341.csv', usecols=[1,2],names=['time','val'], converters= {'time': pd.to_datetime})
for i,entry in enumerate(cd):
    cd[i].sort_values(by=['time'])
    cd[i]['val'].apply(lambda x: (x - cd[i]['val'].mean()) / (cd[i]['val'].max() - cd[i]['val'].min()))
cor=np.zeros([len(cd),len(cd)],float)
for i in range(0,len(cd)):
    for j in range(i,len(cd)):
        joined_mat= cd[i].set_index('time').join(cd[j].set_index('time'), on='time', how='inner', lsuffix='_left',
                                            rsuffix='_right', sort=True)
        cor[i][j]=joined_mat.corr().loc['val_left']['val_right']
        cor[j][i]=cor[i][j]
f = plt.figure(figsize=(6, 6))
plt.matshow(abs(cor), fignum=f.number)
plt.xticks(range(len(entries)), entries, fontsize=12, rotation=90)
plt.yticks(range(len(entries)), entries, fontsize=12)
cb = plt.colorbar()
cb.ax.tick_params(labelsize=14)
plt.title('Correlation between PERCIPITATION sensors', y=1.18)
plt.xlabel('Sensor ID')
plt.ylabel('Sensor ID')
plt.show()
