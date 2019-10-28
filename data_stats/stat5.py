import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf
cd=pd.read_csv('data/Milano_WeatherPhenomena/mi_meteo_5911.csv', usecols=[1,2],names=['time','val'], converters= {'time': pd.to_datetime})
cd.sort_values(by=['time'])
cd['val'].apply(lambda x: (x - cd['val'].mean()) / (cd['val'].max() - cd['val'].min()))
plot_acf(cd['val'], lags=300)
result=seasonal_decompose(cd['val'],model='additive',freq=26)
plt.xlabel('Lag')
plt.ylabel('Auto correlation')
result.plot()
def difference(dataset, interval):
    diff = list()
    for i in range(interval, len(dataset)):
        value = dataset[i] - dataset[i - interval]
        diff.append(value)
    return pd.DataFrame(diff, columns = ['val'])
plt.figure()
cd['val']=difference(cd['val'],24)
cd['val'].plot(kind='line',x='time_step',y='Celsius degree')
plt.xlabel('Time interval')
plt.ylabel('Celsius degree')
plt.show()