import sqlite3
import requests
import pandas as pd
import json

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

    with open("ow.dump.json", 'r') as f:
        data = json.loads(f.read())
    df = pd.json_normalize(data['hourly'])
    print(df)

if __name__ == '__main__':
    zad1()
    # zad2()
    # zad4()