#invite people for the Kaggle party
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import norm
from sklearn.preprocessing import StandardScaler
from scipy import stats


def zad1():
    df_train = pd.read_csv('data_zad7/train.csv')
    total = df_train.isnull().sum().sort_values(ascending=False)
    percent = (df_train.isnull().sum() / df_train.isnull().count()).sort_values(ascending=False)
    missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
    missing_data.head(20)
    df_train = df_train.drop((missing_data[missing_data['Total'] > 1]).index, 1)
    df_train = df_train.drop(df_train.loc[df_train['Electrical'].isnull()].index)
    df_train.isnull().sum().max()
    var = 'OverallQual'
    data = pd.concat([df_train['SalePrice'], df_train[var]], axis=1)
    f, ax = plt.subplots(figsize=(8, 6))
    fig = sns.boxplot(x=var, y="SalePrice", data=data)
    fig.axis(ymin=0, ymax=800000);

    plt.show()


def zad2():
    df_train = pd.read_csv('data_zad7/train.csv')

    Q1 = df_train.quantile(0.25)['SalePrice']
    Q3 = df_train.quantile(0.75)['SalePrice']

    IRQ = Q3 - Q1

    print(Q1)
    print(Q3)
    print(IRQ)

def zad3():
    df_train = pd.read_csv('data_zad7/train.csv')

    df_train.sort_values(by='GrLivArea', ascending=False)[:2]

    df_train = df_train.drop(df_train[df_train['Id'] == 1299].index)
    df_train = df_train.drop(df_train[df_train['Id'] == 524].index)
    var = 'TotalBsmtSF'
    data = pd.concat([df_train['SalePrice'], df_train[var]], axis=1)
    data1 = data[data['TotalBsmtSF']<2000]
    data1.plot.scatter(x=var, y='SalePrice', ylim=(0, 800000));
    plt.show()

def zad4():
    df_train = pd.read_csv('data_zad7/train.csv')
    corrmat = df_train.corr()
    # saleprice correlation matrix
    k = 10  # number of variables for heatmap
    cols = corrmat.nlargest(k, '2ndFlrSF')['2ndFlrSF'].index
    cm = np.corrcoef(df_train[cols].values.T)
    sns.set(font_scale=1.25)
    hm = sns.heatmap(cm, cbar=True, annot=True, square=True, fmt='.2f', annot_kws={'size': 10}, yticklabels=cols.values,
                     xticklabels=cols.values)
    plt.show()

    # print(cm)
    for i in cm[0]:
        if i > 0.6:
            print(i)

def zad5():
    df_train = pd.read_csv('data_zad7/train.csv')
    # correlation matrix
    corrmat = df_train.corr()
    f, ax = plt.subplots(figsize=(12, 9))
    sns.heatmap(corrmat, vmax=.8, square=True)

    plt.show()

if __name__ == '__main__':
    # zad1()
    # zad2()
    # zad3()
    # zad4()
    zad5()