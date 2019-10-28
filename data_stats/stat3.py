
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
#with outlier removal
cd={}
cdl={}
entries=os.listdir('data/Milano_WeatherPhenomena')
for i,entry in enumerate(entries):
    entries[i]=entries[i][9:-4]
    cd[i]=pd.read_csv('data/Milano_WeatherPhenomena/mi_meteo_'+entries[i]+'.csv', usecols=[1,2],names=['time','val'], converters= {'time': pd.to_datetime})
    q1=cd[i]['val'].quantile(0.25)
    q3=cd[i]['val'].quantile(0.75)
    iqr=q3-q1
    cd[i]=cd[i][~((cd[i]['val']<(q1-1.5*iqr)) | (cd[i]['val']>(q3+1.5*iqr)))]
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
f = plt.figure(figsize=(15, 15))
plt.subplot(1,2,1)
plt.imshow(abs(cor))
plt.xticks(range(len(entries)), entries, fontsize=12, rotation=90)
plt.yticks(range(len(entries)), entries, fontsize=12)
plt.ylabel('Sensor ID')
plt.xlabel('Sensor ID')
plt.title('Without outliers', y=1.08)
cb = plt.colorbar()
cb.ax.tick_params(labelsize=14)
#without outlier removal
cd2={}
for i,entry in enumerate(entries):
    cd2[i]=pd.read_csv('data/Milano_WeatherPhenomena/mi_meteo_'+entries[i]+'.csv', usecols=[1,2],names=['time','val'], converters= {'time': pd.to_datetime})
for i,entry in enumerate(cd2):
    cd2[i].sort_values(by=['time'])
    cd2[i]['val'].apply(lambda x: (x - cd2[i]['val'].mean()) / (cd2[i]['val'].max() - cd2[i]['val'].min()))
cor2=np.zeros([len(cd2),len(cd2)],float)
for i in range(0,len(cd2)):
    for j in range(i,len(cd2)):
        joined_mat= cd2[i].set_index('time').join(cd2[j].set_index('time'), on='time', how='inner', lsuffix='_left',
                                            rsuffix='_right', sort=True)
        cor2[i][j]=joined_mat.corr().loc['val_left']['val_right']
        cor2[j][i]=cor2[i][j]
plt.subplot(1,2,2)
plt.imshow(abs(cor2))
plt.xticks(range(len(entries)), entries, fontsize=12, rotation=90)
plt.yticks(range(len(entries)), entries, fontsize=12)
plt.ylabel('Sensor ID')
plt.xlabel('Sensor ID')
plt.title('With outliers', y=1.08)
cb = plt.colorbar()
cb.ax.tick_params(labelsize=14)
plt.show()