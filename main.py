import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.formula.api import ols
import statsmodels.graphics.gofplots as sm



def zad_0():
    data = pd.read_csv('deflection.csv',sep = ';')
    data['Load2'] = data['Load'] ** 2
    model = ols('Deflection ~ Load + Load2', data=data)
    res = model.fit()


    # data['Prediction'] = model.predict(data)
    # ax = data.plot.scatter(x='Load', y='Deflection', ax=axs[0, 0])
    fig, axs = plt.subplots(2, 2, squeeze=False)
    data['Prediction'] = res.predict(data)
    plt.tight_layout()

    ax = data.plot.scatter(x='Load', y='Deflection', ax=axs[0, 0])
    data.plot(x='Load', y='Prediction', ax=axs[0, 0], color='red')
    # plt.subplot(2,2,2)
    residuals = res.predict(data) - data['Deflection']
    axs[0, 1].scatter(data['Deflection'], (residuals))
    axs[0, 1].set_xlabel('Deflection')
    axs[0, 1].set_ylabel('Residual values')

    axs[1, 0].hist(residuals)
    axs[1, 0].set_ylabel('frequency')
    axs[1, 0].set_xlabel('residuual values')
    plt.subplot(2, 2, 4)
    sm.qqplot(residuals, stats.t, distargs=(4,), loc=3, scale=10, fit=True, ax=axs[1, 1], line='s')
    plt.tight_layout()



def zad_1():
    #zad1
    df_train = pd.read_csv('train.csv')
    Q1 = df_train['SalePrice'].quantile(.25)
    Q3 = df_train['SalePrice'].quantile(.75)
    IRQ = Q3 - Q1
    down = Q1 - 1.5 * IRQ
    up = Q3 + 1.5 * IRQ
    df1 = df_train.loc[df_train['SalePrice'] >= down].loc[df_train['SalePrice'] <= up].reset_index()
    data = pd.concat([df1['SalePrice'], df1['GrLivArea']], axis=1)
    print(data)

    model = ols('SalePrice ~ GrLivArea', data=data)
    res = model.fit()
    print(res.summary())

def zad_2():
    #zad2
    df_train = pd.read_csv('train.csv')
    df_train = df_train[df_train['OverallQual'] == 3]
    Q1 = df_train['SalePrice'].quantile(.25)
    Q3 = df_train['SalePrice'].quantile(.75)
    IRQ = Q3 - Q1
    down = Q1 - 1.5 * IRQ
    up = Q3 + 1.5 * IRQ
    df1 = df_train.loc[df_train['SalePrice'] >= down].loc[df_train['SalePrice'] <= up].reset_index()
    data = pd.concat([df1['SalePrice'], df1['GrLivArea']], axis=1)


    model = ols('SalePrice ~ GrLivArea', data=data)
    res = model.fit()
    print(res.summary())

def zad_3():
    df_train = pd.read_csv('train.csv')
    df_train = df_train[df_train['OverallQual'] == 3]
    Q1 = df_train['SalePrice'].quantile(.25)
    Q3 = df_train['SalePrice'].quantile(.75)
    IRQ = Q3 - Q1
    down = Q1 - 1.5 * IRQ
    up = Q3 + 1.5 * IRQ
    df1 = df_train.loc[df_train['SalePrice'] >= down].loc[df_train['SalePrice'] <= up].reset_index()
    data = pd.concat([df1['SalePrice'], df1['GrLivArea'], df1['OverallQual']], axis=1)
    X = data[['OverallQual', 'GrLivArea']]
    y = data['SalePrice']

    X = sm.add_constant(X)
    est = sm.OLS(y, X).fit()
    print(est.summary())

if __name__ == '__main__':
    zad_0()
    zad_1()
    zad_2()
    zad_3()
    plt.show()

