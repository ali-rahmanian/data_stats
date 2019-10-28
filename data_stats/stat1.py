import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
cd={}
entries=os.listdir('data/Milano_WeatherPhenomena')
for i,entry in enumerate(entries):
    entries[i]=entries[i][9:-4]
    cd[i]=pd.read_csv('data/Milano_WeatherPhenomena/mi_meteo_'+entries[i]+'.csv', usecols=[1,2],names=['time','val'], converters= {'time': pd.to_datetime})
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
f = plt.figure(figsize=(10, 12))
plt.matshow(abs(cor), fignum=f.number)
plt.xticks(range(len(entries)), entries, fontsize=12, rotation=90)
plt.yticks(range(len(entries)), entries, fontsize=12)
cb = plt.colorbar()
cb.ax.tick_params(labelsize=14)
plt.xlabel('Sensor ID')
plt.ylabel('Sensor ID')
plt.title('Correlation between sensors', y=1.08)
plt.show()
