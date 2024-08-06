import pandas as pd
import numpy as np
import json
from pandas import json_normalize
import matplotlib.pyplot as plt
from scipy.stats import permutation_test

def zad1():
    # load data using Python JSON module
    df_energy= pd.read_csv('Energy_consumption_Dayton.csv')
    df_energy['date'] = df_energy['Datetime'].str[:-9]
    df_energy['time'] = df_energy['Datetime'].str[-9:]
    # print(df_energy)
    df_energy_day = df_energy.groupby(['date']).sum('Energy_MW')
    df_energy_day = df_energy_day.reset_index()
    print(df_energy_day)
    df_energy_time = df_energy.groupby(['time']).sum('Energy_MW')
    df_energy_time = df_energy_time.reset_index()
    #print(df_energy_time)

    s = pd.date_range('2004-10-01', '2018-08-03', freq='D').to_series()
    df_day_of_week = pd.DataFrame(s.dt.dayofweek)
    df_day_of_week = df_day_of_week.reset_index()
    print(df_day_of_week)

    df_energy_day = df_energy_day.merge(df_day_of_week, left_on='date', right_on='index')
    print(df_energy_day)



    # df_energy_time.plot(x='time', y='Energy_MW')
    # data_days = pd.read_hdf('dayton_energybyday.hdf5')
    # data_days = df_energy.rolling(24).sum()[::24].dropna()
    # data = pd.to_datetime(data_days.index)
    # data_days['weekday'] = data.day_of_week
    # data_days.boxplot(by = 'weekday')




    # def statistic(x, y, axis=0):
    #     return np.mean(x, axis = axis) - np.mean(y, axis = axis)
    # workdays = data_strided.loc[data_strided['weekday']<5, 'Energy_MW']
    # weekends = data_strided.loc[data_strided['weekday']>=5, 'Energy_MW']
    # p_value = permutation_test((workdays, weekends), statistic, n_resamples=999, alternative='greater')




    # data = pd.read_csv('Energy_consumption_Dayton.csv')
    # def statictics(x, y, axis=0):
    #     return np.mean(x, axis=axis) - np.mean(y, axis=axis)
    #
    # workdays = data[]
    # weekend =
    # p_value = permutation_test((workdays, weekend), statictics, n_resamples=999, alternative='greater')
    # data = pd.read_hdf()

if __name__ == '__main__':
    zad1()