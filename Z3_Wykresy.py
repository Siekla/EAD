import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import requests
import json
import random


def zad0():
    x = np.linspace(0, 2, 100)

    fig, ax = plt.subplots()
    ax.plot(x, x)
    ax.plot(x, x ** 2)
    ax.plot(x, x ** 3)

    plt.show()

def zad_1_i_2():
    x = np.linspace(-5, 5, 50)

    #f = (1/(std_dev*np.sqrt(np.pi)))*np.exp((-(x-mean)**2)/(2*std_dev))
    # mean = 0, std_dev = 1
    f1 = (1/(1*np.sqrt(np.pi)))*np.exp((-(x-0)**2)/(2*1))
    # mean = -2, std_dev = 2
    f2 = (1 / (2 * np.sqrt(np.pi))) * np.exp((-(x - -2) ** 2) / (2 * 2))
    # mean = 3, std_dev = 3
    f3 = (1 / (3 * np.sqrt(np.pi))) * np.exp((-(x - 3) ** 2) / (2 * 3))
    # mean = 4, std_dev = 4
    f4 = (1 / (4 * np.sqrt(np.pi))) * np.exp((-(x - 4) ** 2) / (2 * 4))


    fig, ax = plt.subplots()
    ax.plot(x, f1, 'or')
    ax.plot(x, f2, '.b')
    ax.plot(x, f3, '--g')
    ax.plot(x, f4, 'xk')

    ax.set_title('Rozkład Gaussa', fontsize=16)
    ax.set_ylabel('f(x)')
    ax.set_ylim(0, 1)
    ax.set_xlim(-5, 5)
    ax.set_xticks(np.arange(-5, 6, 1))
    ax.grid(color='k', linestyle='-', linewidth=0.1)
    ax.legend(['u=0, a=1', 'u=-2, a=2', 'u=3, a=3', 'u=4, a=4'],loc = 'upper left')

    plt.show()

def zad_3_i_4():

    with open('cancer_survival_in_us.json') as json_file:
        data_dict = json.load(json_file)

    data_df = pd.DataFrame.from_dict(data_dict['age_groups'])

    age = data_df['age'].to_list()
    male_survivors = data_df['male_survivors'].to_list()
    female_survivors = data_df['female_survivors'].to_list()

    print(age)
    print(male_survivors)
    print(female_survivors)
    fig, ax = plt.subplots()

    ax.grid(color='k', linestyle='-', axis='y', linewidth=0.2)
    width = 0.3
    x = np.arange(len(age))
    ax.bar(x - width / 2, male_survivors, width)
    ax.bar(x + width / 2, female_survivors, width, label='Woman')

    labels_x = ['40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85-89', '90+']
    y = [0, 10, 20, 30, 40]
    labels_y = ['0', '10%', '20%', '30%', '40%']


    ax.errorbar(x-0.1, male_survivors, xerr = 0.2, yerr=3, fmt='.k', capsize=2)
    ax.errorbar(x+0.1, female_survivors, xerr=0.2, yerr=3, fmt='.k', capsize=2)
    ax.set_yticks(y)
    ax.set_yticklabels(labels_y)
    ax.set_xticks(x)
    ax.set_xticklabels(labels_x)
    ax.tick_params(axis='x', labelrotation=90)

    ax.legend()
    plt.show()

def zad5():
    df = pd.read_csv('russia2020_vote.csv')

    df["Mean_yes"] = df["yes"]/df["given"]
    fig, ax = plt.subplots()
    ax.hist(df["Mean_yes"], 500, density=True, facecolor='r')
    plt.show()

    # przez to że więcej danych jest brane do Histogramy to również znajduje się tam więcej Picków(wartości które znacznie odbiegają od reszty)

if __name__ == '__main__':
    #zad0()
    #zad_1_i_2()
    zad_3_i_4()
    # zad5()