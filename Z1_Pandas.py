import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandasgui

df = pd.read_csv('population_by_country_2019_2020.csv')

def zad2_pandas():

    print(df.describe())
    print(df)
    pandasgui.show(df, settings={'block': True})
    print(df)

def main():
    df["Net Population change"] = np.abs(df['Population (2020)']-df['Population (2019)'])
    df['Population change [%]'] = np.abs(((df['Population (2020)']-df['Population (2019)'])/df['Population (2020)'])*100)


    df.sort_values("Population change [%]",axis=0,inplace=True,ascending=False)
    df.iloc[0:9].plot(kind="bar", x="Country (or dependency)", y=["Population (2020)", "Population (2019)"])
    plt.show()

    df["Density (2020)"] = "Low"

    gest_zalud = df.loc[:, "Population (2020)"] / df.loc[:, "Land Area (Km²)"]
    pom_z = len(gest_zalud)

    for i in range(pom_z):
        if gest_zalud[i] > 500:
            df.loc[i, "Density (2020)"] = "High"
            i += 1
        else:
            i += 1

    df.iloc[0::2, :].to_csv("population_output.csv")

if __name__ == '__main__':
    #zad2_pandas()
    main()