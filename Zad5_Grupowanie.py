import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def zad1():
    data = pd.read_csv('city_temperature.csv')

    df = data.drop(columns=['Day']).pivot_table(columns='Region', index=['Year', 'Month'],
                                                aggfunc=['min', 'max', 'mean'], values='AvgTemperature')
    print(df)

def zad2():
    data = pd.read_csv('city_temperature.csv')

    df = data.drop(columns=['Day', 'Year', 'Country', 'State', 'City'])
    df = df.pivot_table(columns='Region', index=['Month'], aggfunc=['mean'], values=['AvgTemperature'])

    df1 = df.loc[12, slice(None)]
    df2 = df.loc[6, slice(None)]

    fig, axes = plt.subplots(nrows=2, ncols=1)
    df1.plot(ax=axes[0])
    df2.plot(ax=axes[1])
    plt.show()


def zad3():
    data = pd.read_csv('titanic_train.csv')

    df = data.drop(columns=['Name', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked'])
    df1 = df.pivot_table(columns=['Pclass', 'Sex'], aggfunc=['mean'], values=['Survived'])
    df2 = df.pivot_table(columns=['Sex', 'Survived', 'Pclass'], index=['Sex', 'Pclass'], aggfunc=['count'], values=['Sex', 'Pclass'])

    df2.T.plot(kind='bar')

    plt.show()
    #print(df)
    print('Osoby ktore przezyly z podziealem na plec i klase',df1)
    print('Procentowy udzial osob ktore przyzyly z uwzglednieniem plci i klasy biletu',df2)

if __name__ == '__main__':
    #zad1()
    #zad2()
    zad3()


