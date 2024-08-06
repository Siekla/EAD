import sqlite3
import pandas as pd
import requests
import json
from pandas import json_normalize
from datetime import datetime
import matplotlib.pyplot as plt

def zad1():
    conn = sqlite3.connect("Chinook_Sqlite.sqlite")  # połączenie do bazy danych - pliku
    c = conn.cursor()

    for row in c.execute('SELECT Track.Name, Album.Title FROM Track INNER JOIN Album ON Track.AlbumId = Album.AlbumId'):
        print(row)


    conn.close()


def zad2():
    conn = sqlite3.connect("Chinook_Sqlite.sqlite")  # połączenie do bazy danych - pliku
    c = conn.cursor()

    for row in c.execute('SELECT Artist.Name, Album.Title FROM Album JOIN Artist ON ALbum.ArtistId = Artist.ArtistId'):
        print(row)

    conn.close()

def zad4():
    with open('data.json', 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)

    df2 = pd.DataFrame.from_dict(json_object["data"])
    tab = pd.DataFrame()
    tab["Data"] = df2["dt"]
    dt = df2["dt"]

    for i in tab.index:
        dat = dt.at[i]
        main = df2["main"][i]
        wind = df2["wind"][i]
        tab.at[i, "Data"] = pd.to_datetime(dat, unit='s')
        tab.at[i, "Temp"] = main["temp"] - 273
        tab.at[i, "Humidity"] = main["humidity"]
        tab.at[i, "Wind speed"] = wind["speed"]
        # tab.at
    # print(tab)
    obas = pd.DataFrame(tab)
    obas.plot(x = "Data", y = "Temp", xlabel = 'Data', ylabel = 'Temperature')
    plt.show()

    # url = "https://api.openweathermap.org/data/2.5/weather"
    # api_key = "f3bf5e62ceaf501e451d2eb1560507a4"
    # latitude = 52.2661111312009
    # longitude = 18.426405457524865
    # req = requests.get(f"{url}?lat={latitude}&lon={longitude}&exclude=hourly,daily&units=metric&appid={api_key}")
    # print(req.text)



if __name__ == '__main__':
    #zad1()
    #zad2()
    zad4()