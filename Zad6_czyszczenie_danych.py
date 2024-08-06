import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
import fuzzywuzzy.process
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import LabelBinarizer



def score_dataset(x_train, x_valid, y_train, y_valid):
    model = RandomForestRegressor(n_estimators=100, random_state=0)
    model.fit(x_train, y_train)
    preds = model.predict(x_valid)
    return mean_absolute_error(y_valid, preds)


def replace_matches_in_column(df, column, string_to_match, min_ratio=90):
    # get a list of unique strings
    strings = df[column].unique()

    # get the top 10 closest matches to our input string
    matches = fuzzywuzzy.process.extract(string_to_match, strings,
                                         limit=10, scorer=fuzzywuzzy.fuzz.token_sort_ratio)

    # only get matches with a ratio > 90
    close_matches = [matches[0] for matches in matches if matches[1] >= min_ratio]

    # get the rows of all the close matches in our dataframe
    rows_with_matches = df[column].isin(close_matches)

    # replace all rows with close matches with the input matches
    df.loc[rows_with_matches, column] = string_to_match

def zad0():
    df = pd.read_csv('melb_data.csv')
    train_df, test_df = train_test_split(df, test_size=0.7)


    train_df_cleaned = train_df.dropna(axis=1)
    test_df_cleaned = train_df.dropna(axis=1)
    cols_x = train_df_cleaned.select_dtypes(include=[np.number]).columns.difference(['Price'])  # wybiera tylko kolumny z wartosciami numerycznymi, za wyjątkiem kolumny z wartością referencyjną - wejście do klasyfikatora
    cols_y = 'Price'  # - wyjście z klasyfikatora
    print('Usuniecie wierszy', score_dataset(train_df_cleaned[cols_x], test_df_cleaned[cols_x], train_df_cleaned[cols_y], test_df_cleaned[cols_y]))


    train_df_cleaned = train_df.dropna()
    test_df_cleaned = train_df.dropna()
    cols_x = train_df_cleaned.select_dtypes(include=[np.number]).columns.difference(['Price'])  # wybiera tylko kolumny z wartosciami numerycznymi, za wyjątkiem kolumny z wartością referencyjną - wejście do klasyfikatora
    cols_y = 'Price'  # - wyjście z klasyfikatora
    print('Usuniecie kolumn', score_dataset(train_df_cleaned[cols_x], test_df_cleaned[cols_x], train_df_cleaned[cols_y], test_df_cleaned[cols_y]))


    train_df_cleaned = df.fillna(0)
    test_df_cleaned = df.fillna(0)
    cols_x = train_df_cleaned.select_dtypes(include=[np.number]).columns.difference(['Price'])  # wybiera tylko kolumny z wartosciami numerycznymi, za wyjątkiem kolumny z wartością referencyjną - wejście do klasyfikatora
    cols_y = 'Price'  # - wyjście z klasyfikatora
    print('Uzupełnienie braków 0', score_dataset(train_df_cleaned[cols_x], test_df_cleaned[cols_x], train_df_cleaned[cols_y], test_df_cleaned[cols_y]))


    train_df_cleaned = df.fillna(method='bfill', axis=0).fillna(0)
    test_df_cleaned = df.fillna(method='bfill', axis=0).fillna(0)
    cols_x = train_df_cleaned.select_dtypes(include=[np.number]).columns.difference(['Price'])  # wybiera tylko kolumny z wartosciami numerycznymi, za wyjątkiem kolumny z wartością referencyjną - wejście do klasyfikatora
    cols_y = 'Price'  # - wyjście z klasyfikatora
    print('Uzupełnienie braków wartością sąsiednią', score_dataset(train_df_cleaned[cols_x], test_df_cleaned[cols_x], train_df_cleaned[cols_y], test_df_cleaned[cols_y]))

    imp_mean = SimpleImputer(missing_values=np.nan, strategy='mean')
    df_train_numeric = train_df.select_dtypes(include=[np.number]).copy()
    df_test_numeric = test_df.select_dtypes(include=[np.number]).copy()  # wybór tylko kolumn przechowujacych liczby, należy wykonać kopię obiektu
    df_train_numeric.loc[:] = imp_mean.fit_transform(df_train_numeric)  # dopasowanie parametrów (średnich) i transformacja zbioru uczącego
    df_test_numeric[:] = imp_mean.transform(df_test_numeric)  # zastosowanie modelu do transformacji zbioru testowego (bez wyznaczania parametrów)
    cols_x = train_df_cleaned.select_dtypes(include=[np.number]).columns.difference(['Price'])  # wybiera tylko kolumny z wartosciami numerycznymi, za wyjątkiem kolumny z wartością referencyjną - wejście do klasyfikatora
    cols_y = 'Price'  # - wyjście z klasyfikatora
    print('uzupełnienie braków medianą', score_dataset(train_df_cleaned[cols_x], test_df_cleaned[cols_x], train_df_cleaned[cols_y], test_df_cleaned[cols_y]))



    # Make copy to avoid changing original data
    label_train = train_df.dropna().copy()
    label_test = test_df.dropna().copy()

    label_encoder = LabelEncoder()
    col = 'CouncilArea'
    label_train[col] = label_encoder.fit_transform(label_train[col])
    label_test[col] = label_encoder.transform(label_test[col])

    label_binarizer = LabelBinarizer()

    col = 'CouncilArea'
    lb_results = label_binarizer.fit_transform(label_train[col])
    lb_results_df = pd.DataFrame(lb_results, columns=label_binarizer.classes_)
    print(lb_results_df)
    print(len(lb_results_df.columns))
    print(lb_results_df.columns)
    for i in range(len(lb_results_df.columns)):
        label_train[i] = lb_results_df[i]
        label_test[i] = lb_results_df[i]

    label_train = label_train.fillna(0)
    label_test = label_test.fillna(0)
    cols_x = label_train.select_dtypes(include=[np.number]).columns.difference(['Price'])
    cols_y = 'Price'  # - wyjście z klasyfikatora
    print('dodanie nowej cechy (CouncilArea) za pomocą LabelBinarizer', score_dataset(label_train[cols_x], label_test[cols_x], label_train[cols_y], label_test[cols_y]))


def task01_e():
    df = pd.read_csv("melb_data.csv")
    print(df.columns)
    train_df, test_df = train_test_split(df, test_size=0.7)

    # Make copy to avoid changing original data
    label_train = train_df.dropna().copy()
    label_test = test_df.dropna().copy()

    label_encoder = LabelEncoder()
    col = 'CouncilArea'
    label_train[col] = label_encoder.fit_transform(label_train[col])
    label_test[col] = label_encoder.transform(label_test[col])

    label_binarizer = LabelBinarizer()

    col = 'CouncilArea'
    lb_results = label_binarizer.fit_transform(label_train[col])
    lb_results_df = pd.DataFrame(lb_results, columns=label_binarizer.classes_)
    print(lb_results_df)

    print(len(lb_results_df.columns))
    print(lb_results_df.columns)
    for i in range(len(lb_results_df.columns)):
        label_train[i] = lb_results_df[i]
        label_test[i] = lb_results_df[i]

    label_train = label_train.fillna(0)
    label_test = label_test.fillna(0)
    cols_x = label_train.select_dtypes(include=[np.number]).columns.difference(['Price'])
    cols_y = 'Price'  # - wyjście z klasyfikatora
    print(score_dataset(label_train[cols_x], label_test[cols_x], label_train[cols_y], label_test[cols_y]))


def zad1():
    df = pd.read_csv('melb_data.csv')

    df.loc[:, "Datetime"] = pd.to_datetime(df.loc[:, "Date"], infer_datetime_format=True, format = "%m/%d/%Y")
    df.loc[:, "Day of week"] = df.loc[:, "Datetime"].dt.dayofweek
    print(df["Day of week"])

    plt.hist(df["Day of week"])

    plt.show()

def zad2():
    df = pd.read_csv('melb_data_distorted.csv')

    lista_suburb = df["Suburb"]
    print(lista_suburb)
    uniq_suburb = []
    for i in lista_suburb:
        if i not in uniq_suburb:
            uniq_suburb.append(i)

    print(uniq_suburb)

    for i in uniq_suburb:
        replace_matches_in_column(df, "Suburb", i)

    print(df)


if __name__ == '__main__':
    # zad0()
    # zad1()
    zad2()

