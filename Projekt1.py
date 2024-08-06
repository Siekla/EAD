import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
import sqlite3
import pylab


# zad1
files_folder = "data/"
files_df = pd.DataFrame()

for file in glob.glob(os.path.join(files_folder, "*.txt")):
    files = pd.read_csv(file, names=['name', 'sex', 'count'])
    file_n = int(''.join(filter(str.isdigit, file)))
    files["year"] = file_n
    files_df = pd.concat([files_df, files])
    # print(files_df)

def zad1():
    # wczytuje każdy plik txt używająć funkcji glob i odrazu tworze z nich tablice w Pandasie, a następnie użyuwając Funkcji Concat dorzucam tam kolejne wiersze mojej tablicy
    print('ZAD1:', files_df)

def zad2():

    print("ZAD2\nIlość unikalnych imion lacznie: ", len(files_df['name'].unique()))

def zad3():
    # dziele zbiór dzięki kolumnie sex i zliczam unikatowe imiona
    df_zad3 = files_df.drop(columns=['count', 'year'])
    # print(df_zad3)
    df_zad3_M = df_zad3.loc[lambda df_zad3: df_zad3['sex'] == 'M']
    print("Zad3: Faceci", len(df_zad3_M['name'].unique()))
    df_zad3_M = df_zad3.loc[lambda df_zad3: df_zad3['sex'] == 'F']
    print("Zad3: Kobiety", len(df_zad3_M['name'].unique()))

def zad4():
    # dziele zbiór na płcie
    df_4 = files_df

    all_people_per_year_Male = df_4.loc[(df_4["sex"] == 'M')]
    sum_all_Male = all_people_per_year_Male.groupby(['year']).sum('count') # sumuje wszyskich facetów

    all_people_per_year_Female = df_4.loc[(df_4["sex"] == 'F')]
    sum_all_Female = all_people_per_year_Female.groupby(['year']).sum('count')

    df_4_merged_Male = all_people_per_year_Male.merge(sum_all_Male, left_on='year', right_on='year')
    df_4_merged_Male['frequency_male'] = df_4_merged_Male['count_x']/df_4_merged_Male['count_y'] # dziele ilość facetów mających konkretne imie przez sume wszyskich facetów
    print('ZAD4 Male:\n', df_4_merged_Male)

    df_4_merged_Female = all_people_per_year_Female.merge(sum_all_Female, left_on='year', right_on='year')
    df_4_merged_Female['frequency_female'] = df_4_merged_Female['count_x']/df_4_merged_Female['count_y']
    print('ZAD4 Female:\n', df_4_merged_Female)

def zad5():


    df_5 = files_df

    sum_all = df_5.groupby(['year']).sum('count')

    SM = sum_all.reset_index()

    all_people_per_year_Male = df_5.loc[(df_5["sex"] == 'M')]
    sum_all_Male = all_people_per_year_Male.groupby(['year']).sum('count')
    all_people_per_year_Female = df_5.loc[(df_5["sex"] == 'F')]
    sum_all_Female = all_people_per_year_Female.groupby(['year']).sum('count')

    sex_diff = sum_all_Male.merge(sum_all_Female, left_on='year', right_on='year')
    sex_diff['SEX_DIFF'] = sex_diff["count_x"]-sex_diff["count_y"]
    SMX = sex_diff.reset_index()

    SMX_abs = SMX.abs()
    min_SMX = SMX_abs['SEX_DIFF'].min()
    max_SMX = SMX_abs['SEX_DIFF'].max()

    x_1 = SM['year']
    y_1 = SM['count']

    x_2 = SMX['year']
    y_2 = SMX['SEX_DIFF']

    fig,axs = plt.subplots(2, 1)
    axs[0].set_title('Urodzenia w danym roku')
    axs[0].plot(x_1, y_1)

    axs[1].set_title('Stosunek urodzeń między chłopcami a dziewczynkami')
    axs[1].plot(x_2, y_2)

    rok_SM_max = SMX_abs.loc[lambda SMX_abs: SMX_abs['SEX_DIFF'] == max_SMX]
    rok_SM_min = SMX_abs.loc[lambda SMX_abs: SMX_abs['SEX_DIFF'] == min_SMX]
    rok_SM_min = rok_SM_min.drop(columns = ['count_x', 'count_y'])
    rok_SM_max = rok_SM_max.drop(columns=['count_x', 'count_y'])

    print('\nZAD5: \nNajwiększa różnica miedzy płciami:\n', rok_SM_max)
    print('\nZAD5: \nNajmniejsza różnicy miedzy płciami:\n',rok_SM_min)

    fig = pylab.gcf()
    fig.canvas.manager.set_window_title('Zad5')

    plt.show()


def zad6():

    df_6 = files_df
    # sprawdzam popularność danego imienia w każdym z lat a następnie bezwzględnie je sumuje
    # #Male
    all_people_per_year_Male = df_6.loc[(df_6["sex"] == 'M')]
    sum_all_Male = all_people_per_year_Male.groupby(['year']).sum('count')
    df_6_merged_Male = all_people_per_year_Male.merge(sum_all_Male, left_on='year', right_on='year')
    df_6_merged_Male['frequency_male'] = df_6_merged_Male['count_x']/df_6_merged_Male['count_y']
    # print(df_6_merged_Male)
    df_6_merged_Male = df_6_merged_Male.sort_values(by='frequency_male')
    df_6_merged_Male = df_6_merged_Male.drop(columns = ['sex', 'count_x', 'year', 'count_y'])
    df_6_grouped_M = df_6_merged_Male.groupby('name').sum()
    df_6_grouped_M = df_6_grouped_M.reset_index()
    df6_sort_M = df_6_grouped_M.sort_values(by='frequency_male',ascending=False)
    #print(df6_sort_M)
    df_6_1000_M = df6_sort_M.iloc[0:1001, :]
    print('\nZAD6\nTop 1000 imion Mężczyzn\n', df_6_1000_M)



    #Female
    all_people_per_year_Female = df_6.loc[(df_6["sex"] == 'F')]
    sum_all_Female = all_people_per_year_Female.groupby(['year']).sum('count')
    df_6_merged_Female = all_people_per_year_Female.merge(sum_all_Female, left_on='year', right_on='year')
    df_6_merged_Female['frequency_female'] = df_6_merged_Female['count_x']/df_6_merged_Female['count_y']
    df_6_merged_Female.sort_values(by='frequency_female')
    df_6_merged_Female = df_6_merged_Female.drop(columns = ['sex', 'count_x', 'year', 'count_y'])
    df_6_grouped_F = df_6_merged_Female.groupby('name').sum()
    df_6_grouped_F = df_6_grouped_F.reset_index()
    df6_sort_F = df_6_grouped_F.sort_values(by='frequency_female',ascending=False)
    df_6_1000_F = df6_sort_F.iloc[0:1001, :]
    print('\nZAD6\nTop 1000 imion Kobiet\n', df_6_1000_F)


    #All

    df_M = df_6_1000_M.rename(columns = {'frequency_male':'frequency_all'})
    df_F = df_6_1000_F.rename(columns = {'frequency_female':'frequency_all'})

    df_6_both_C = pd.concat([df_M, df_F])
    # print(df_6_both_C)
    df_6_both_g = df_6_both_C.sort_values(by='frequency_all', ascending=False)
    # print(df_6_both_g)
    df_6_both = df_6_both_g.iloc[0:1000, :]
    print('\nZAD6\nTop 1000 imion ogólnie\n', df_6_both)




def zad7():

    df_7 = files_df
    # wyznaczam najpopularniejsze imie Damskie tak samo jak w zadaniu 6
    all_people_per_year_Female = df_7.loc[(df_7["sex"] == 'F')]
    sum_all_Female = all_people_per_year_Female.groupby(['year']).sum('count')
    df_7_merged_Female = all_people_per_year_Female.merge(sum_all_Female, left_on='year', right_on='year')
    df_7_merged_Female['frequency_female'] = df_7_merged_Female['count_x']/df_7_merged_Female['count_y']
    Mary_percent = df_7_merged_Female.loc[lambda df_7_merged_Female: df_7_merged_Female['name'] == 'Mary']
    Mary_percent = Mary_percent.drop(columns=['name', 'sex', 'count_x', 'count_y'])
    #print(Mary_percent)

    df_7_merged_Female.sort_values(by='frequency_female')
    df_7_merged_Female = df_7_merged_Female.drop(columns = ['sex', 'count_x', 'year', 'count_y'])
    df_7_grouped_F = df_7_merged_Female.groupby('name').sum()
    df_7_sort_F = df_7_grouped_F.sort_values(by='frequency_female', ascending=False)
    df_7_1000_F = df_7_sort_F.iloc[0:1001, :]
    #print(df_7_1000_F)  # Najpopularniejsze Damskie imie to Mary


    # Następnie korzystając z funkcji loc[lambda] zbieram lata oraz ilosc danego imienia i wykreślam to na wykresie

    #Mary
    df_7_M = df_7.loc[(df_7["sex"] == 'F')]
    df_7_DMary = df_7_M.drop(columns=['sex'])
    DF_Mary = df_7_DMary.loc[lambda df_7_DMary: df_7_DMary['name'] == 'Mary']
    #print('Mary: \n', DF_Mary)

    #John
    df_7_man = df_7.loc[(df_7["sex"] == 'M')]
    df_7_DJohn = df_7_man.drop(columns=['sex'])
    DF_John = df_7_DJohn.loc[lambda df_7_DJohn: df_7_DJohn['name'] == 'John']
    #print('John: \n', DF_John)

    #John percent
    all_people_per_year_Male = df_7.loc[(df_7["sex"] == 'M')]
    sum_all_Male = all_people_per_year_Male.groupby(['year']).sum('count')
    df_6_merged_Male = all_people_per_year_Male.merge(sum_all_Male, left_on='year', right_on='year')
    df_6_merged_Male['frequency_male'] = df_6_merged_Male['count_x'] / df_6_merged_Male['count_y']
    John_percent = df_6_merged_Male.loc[lambda df_6_merged_Male: df_6_merged_Male['name'] == 'John']
    John_percent = John_percent.drop(columns=['name', 'sex', 'count_x', 'count_y'])
    #print(John_percent)


    x_1 = DF_John['year']
    y_1 = DF_John['count']
    y_1_P = John_percent['frequency_male']

    x_2 = DF_Mary['year']
    y_2 = DF_Mary['count']
    y_2_P = Mary_percent['frequency_female']

    fig, ax = plt.subplots()
    ax.plot(x_1, y_1, color='blue')
    ax.plot(x_2, y_2, color='red')
    ax.set_xlabel("year", color="black", fontsize=14)
    ax.set_ylabel("Amount of names", color="black", fontsize=14)
    ax2 = ax.twinx()
    ax2.plot(x_1, y_1_P, '--b')
    ax2.plot(x_2, y_2_P, '--r')
    ax2.set_ylabel("Popularity of name", color="black", fontsize=14)


    # ponownie korzystając z loc[lambda] wyposuje wszyskie informacje dla wybranych lat

    print('Zad7 \nCount John in 1935 = \n', DF_John.loc[lambda DF_John: DF_John['year'] == 1935], '\n\n')
    print('Count John in 1979 = \n', DF_John.loc[lambda DF_John: DF_John['year'] == 1979], '\n\n')
    print('Count John in 2021 = \n', DF_John.loc[lambda DF_John: DF_John['year'] == 2021], '\n\n')

    print('Count Mary in 1935 = \n', DF_Mary.loc[lambda DF_Mary: DF_Mary['year'] == 1935], '\n\n')
    print('Count Mary in 1979 = \n', DF_Mary.loc[lambda DF_Mary: DF_Mary['year'] == 1979], '\n\n')
    print('Count Mary in 2021 = \n', DF_Mary.loc[lambda DF_Mary: DF_Mary['year'] == 2021], '\n\n')

    fig = pylab.gcf()
    fig.canvas.manager.set_window_title('Zad7')
    plt.legend(['John', 'Mary'], loc='upper right', title='Legend')
    plt.show()


def zad8():

    df_8 = files_df
    # wyznaczam imiona należace do Top1000, sumuje ich wartości i następnie porównuje je z wszyskimi imionami

    # Male
    all_people_per_year_Male = df_8.loc[(df_8["sex"] == 'M')]
    sum_all_Male = all_people_per_year_Male.groupby(['year']).sum('count')
    df_8_merged_Male = all_people_per_year_Male.merge(sum_all_Male, left_on='year', right_on='year')
    df_8_merged_Male['frequency_male'] = df_8_merged_Male['count_x']/df_8_merged_Male['count_y']
    df_8_merged_Male = df_8_merged_Male.sort_values(by='frequency_male', ascending=False)
    df_8_merged_Male = df_8_merged_Male.drop(columns = ['sex', 'count_x', 'count_y'])
    df_top1000_Male = df_8_merged_Male.iloc[0:1000, :]
    grouped_by_year_Male = df_top1000_Male.groupby(['year']).sum('frequency_male')
    # Stworzyłem wykres który przedstawia współczynnikiem imion należących do rankingu Top100,
    # ale gdybyco to jest funkcja która stworzyła by wykres różnorodności imion Męskich
    # grouped_by_year_Male['frequency_male'] = 1 - grouped_by_year_Male['frequency_male']
    grouped_by_year_Male = grouped_by_year_Male.reset_index()
    #print(grouped_by_year_Male)

    # Female
    all_people_per_year_Female = df_8.loc[(df_8["sex"] == 'F')]
    sum_all_Female = all_people_per_year_Female.groupby(['year']).sum('count')
    df_8_merged_Female = all_people_per_year_Female.merge(sum_all_Female, left_on='year', right_on='year')
    df_8_merged_Female['frequency_Female'] = df_8_merged_Female['count_x']/df_8_merged_Female['count_y']
    df_8_merged_Female = df_8_merged_Female.sort_values(by='frequency_Female', ascending=False)
    df_8_merged_Female = df_8_merged_Female.drop(columns = ['sex', 'count_x', 'count_y'])
    df_top1000_Female = df_8_merged_Female.iloc[0:1000, :]
    grouped_by_year_Female = df_top1000_Female.groupby(['year']).sum('frequency_Female')
    # grouped_by_year_Female['frequency_Female'] = 1 - grouped_by_year_Female['frequency_Female'] # Różnorodność imion damskich
    grouped_by_year_Female = grouped_by_year_Female.reset_index()
    #print(grouped_by_year_Female)

    fig, ax = plt.subplots()
    ax.plot(grouped_by_year_Male['year'], grouped_by_year_Male['frequency_male'], color='blue')
    ax.plot(grouped_by_year_Female['year'], grouped_by_year_Female['frequency_Female'], color='red')

    fig = pylab.gcf()
    fig.canvas.manager.set_window_title('Zad8')
    ax.set_title('Współczynnik imion należących do rankingu TOP 1000')
    plt.legend(['Male', 'Female'], loc='upper right', title='Legend')

    grouped_by_year_Male['highest_diff'] = abs(grouped_by_year_Male['frequency_male'] - grouped_by_year_Female['frequency_Female'])
    max_diff_Male = grouped_by_year_Male['highest_diff'].max()
    grouped_by_year_Male = grouped_by_year_Male.drop(columns = ['frequency_male'])
    print('Highest diff = \n', grouped_by_year_Male.loc[lambda grouped_by_year_Male: grouped_by_year_Male['highest_diff'] == max_diff_Male], '\n\n')

    plt.show()

def zad9():

    df_9 = files_df

    all_people_per_year_Male = df_9.loc[(df_9["sex"] == 'M')]
    all_people_per_year_Male['Last_charakter_in_name'] = all_people_per_year_Male['name'].str[-1:] # wyznaczam ostatnia litere imienia (nie wiem czemu ten bład mi wyskakuje ale żadnych błędów nie powodował więc go pominołem)

    all_people_per_year_Male = all_people_per_year_Male.drop(columns=['name', 'sex'])
    df = all_people_per_year_Male



    all = df.groupby(by = ['year']).sum()

    charakter_1 = df.loc[lambda df: df['Last_charakter_in_name'] == 'n'] # z wykresu stworzonego wcześniej funkcją Loc[lambda] wykreślam ilość litery n przez wszyskie lata
    charakter_1 = charakter_1.groupby(by = ['year']).sum()
    charakter_1 = charakter_1.reset_index()
    charakter_1 = charakter_1.merge(all, left_on='year', right_on='year')
    charakter_1['percent'] = charakter_1['count_x']/charakter_1['count_y']
    # print(charakter_1)
    charakter_2 = df.loc[lambda df: df['Last_charakter_in_name'] == 'd']
    charakter_2 = charakter_2.groupby(by=['year']).sum()
    charakter_2 = charakter_2.reset_index()
    charakter_2 = charakter_2.merge(all, left_on='year', right_on='year')
    charakter_2['percent'] = charakter_2['count_x']/charakter_2['count_y']
    # print(charakter_2)
    charakter_3 = df.loc[lambda df: df['Last_charakter_in_name'] == 'y']
    charakter_3 = charakter_3.groupby(by=['year']).sum()
    charakter_3 = charakter_3.reset_index()
    charakter_3 = charakter_3.merge(all, left_on='year', right_on='year')
    charakter_3['percent'] = charakter_3['count_x']/charakter_3['count_y']
    # print(charakter_3)

    #print(charakter_1)
    fig, ax = plt.subplots()

    ax.plot(charakter_1['year'], charakter_1['percent'], color='r')
    ax.plot(charakter_2['year'], charakter_2['percent'], color='g')
    ax.plot(charakter_3['year'], charakter_3['percent'], color='b')

    plt.legend(['n', 'd', 'y'], loc='upper left', title='Legend')
    fig = pylab.gcf()
    fig.canvas.manager.set_window_title('Zad9.1')


    p_loc_1916 = df.loc[lambda df: df['year'] == 1916]
    p_loc_1966 = df.loc[lambda df: df['year'] == 1966]
    p_loc_2021 = df.loc[lambda df: df['year'] == 2021]

    p_group_alfabet_1916 = p_loc_1916.groupby(by = ['Last_charakter_in_name']).sum() # sumuje ilości dnaych imion w wybranym roku
    p_group_alfabet_1966 = p_loc_1966.groupby(by = ['Last_charakter_in_name']).sum()
    p_group_alfabet_2021 = p_loc_2021.groupby(by = ['Last_charakter_in_name']).sum()
    p_group_alfabet_1916 = p_group_alfabet_1916.reset_index()
    p_group_alfabet_1966 = p_group_alfabet_1966.reset_index()
    p_group_alfabet_2021 = p_group_alfabet_2021.reset_index()

    p_group_alfabet_1916 = p_group_alfabet_1916.drop(columns = 'year')
    p_group_alfabet_1966 = p_group_alfabet_1966.drop(columns='year')
    p_group_alfabet_2021 = p_group_alfabet_2021.drop(columns='year')

    DF_all = p_group_alfabet_1916
    DF_all = DF_all.merge(p_group_alfabet_1966, left_on='Last_charakter_in_name', right_on='Last_charakter_in_name') # merguje wszyskie wartości do jednego DF i następnie je wypisuje barplotem
    DF_all = DF_all.merge(p_group_alfabet_2021, left_on='Last_charakter_in_name', right_on='Last_charakter_in_name')
    DF_all = DF_all.rename(columns = {'count_x':'1916', 'count_y':'1966', 'count':'2021'})

    DF_all = DF_all.set_index('Last_charakter_in_name')
    DF_all.plot(kind = 'bar')

    plt.legend(['1916', '1966', '2021'], loc='upper right', title='Legend')
    fig = pylab.gcf()
    fig.canvas.manager.set_window_title('Zad9.2')
    plt.show()


def zad10():

    df_10 = files_df
    #dziele DF na jeden który jest do 1930 i drugi który jest po 2000
    #all_People
    all_people = df_10.reset_index()
    all_people = all_people.drop(columns=['index'])
    all_people_1930 = all_people.loc[all_people['year'] < 1931]
    all_people_2000 = all_people.loc[all_people['year'] > 1999]

    # Wyznaczam Top 1000 dla mężczyzn, kobiet, wspólnie oraz dla lat przed 1930 i po 2000
    #all people 1930
    all_people_1930 = all_people_1930.drop(columns = 'year')
    all_people_1930 = all_people_1930.groupby(['name']).sum('count')
    all_people_1930 = all_people_1930.reset_index()
    all_people_1930 = all_people_1930.sort_values(by='count', ascending=False)
    Top1000_all_people_1930 = all_people_1930.iloc[0:1000, :]
    # print(Top1000_all_people_1930)

    #all people 2000
    all_people_2000 = all_people_2000.drop(columns = 'year')
    all_people_2000 = all_people_2000.groupby(['name']).sum('count')
    all_people_2000 = all_people_2000.reset_index()
    all_people_2000 = all_people_2000.sort_values(by='count', ascending=False)
    Top1000_all_people_2000 = all_people_2000.iloc[0:1000, :]
    # print(Top1000_all_people_2000)

    # Male
    all_Male =df_10.loc[(df_10["sex"] == 'M')]
    all_Male = all_Male.reset_index()
    all_Male = all_Male.drop(columns=['index'])
    all_Male_1930 = all_Male.loc[all_Male['year'] < 1931]
    all_Male_2000 = all_Male.loc[all_Male['year'] > 1999]

    all_Male_1930 = all_Male_1930.drop(columns='year')
    all_Male_1930 = all_Male_1930.groupby(['name']).sum('count')
    all_Male_1930 = all_Male_1930.reset_index()
    all_Male_1930 = all_Male_1930.sort_values(by='count', ascending=False)
    Top1000_all_Male_1930 = all_Male_1930.iloc[0:1000, :]
    # print(Top1000_all_Male_1930)

    all_Male_2000 = all_Male_2000.drop(columns='year')
    all_Male_2000 = all_Male_2000.groupby(['name']).sum('count')
    all_Male_2000 = all_Male_2000.reset_index()
    all_Male_2000 = all_Male_2000.sort_values(by='count', ascending=False)
    Top1000_all_Male_2000 = all_Male_2000.iloc[0:1000, :]
    # print(Top1000_all_Male_2000)



    #Female
    all_Female =df_10.loc[(df_10["sex"] == 'F')]
    all_Female = all_Female.reset_index()
    all_Female = all_Female.drop(columns=['index'])
    all_Female_1930 = all_Female.loc[all_Female['year'] < 1931]
    all_Female_2000 = all_Female.loc[all_Female['year'] > 1999]

    all_Female_1930 = all_Female_1930.drop(columns='year')
    all_Female_1930 = all_Female_1930.groupby(['name']).sum('count')
    all_Female_1930 = all_Female_1930.reset_index()
    all_Female_1930 = all_Female_1930.sort_values(by='count', ascending=False)
    Top1000_all_Female_1930 = all_Female_1930.iloc[0:1000, :]
    # print(Top1000_all_Female_1930)

    all_Female_2000 = all_Female_2000.drop(columns='year')
    all_Female_2000 = all_Female_2000.groupby(['name']).sum('count')
    all_Female_2000 = all_Female_2000.reset_index()
    all_Female_2000 = all_Female_2000.sort_values(by='count', ascending=False)
    Top1000_all_Female_2000 = all_Female_2000.iloc[0:1000, :]
    # print(Top1000_all_Female_2000)

    # Wszystkie te wartości Merguje w 2 DF jeden przed 1930 i drugi po 2000

    everything_1930 = Top1000_all_people_1930.merge(Top1000_all_Male_1930, left_on='name', right_on='name').merge(Top1000_all_Female_1930, left_on='name', right_on='name')
    everything_2000 = Top1000_all_people_2000.merge(Top1000_all_Male_2000, left_on='name', right_on='name').merge(Top1000_all_Female_2000, left_on='name', right_on='name')

    everything_1930 = everything_1930.rename(columns={'count_y': 'male', 'count_x':'all', 'count':'female'})
    everything_2000 = everything_2000.rename(columns={'count_y': 'male', 'count_x': 'all', 'count': 'female'})

    # Wyznaczam ilość konkretnego imienia wsród facetów odejmuje od niego ilość wystąpienia tego imienia wśród kobiet i dziele przez sume występowania tego imienia
    # Jeśli imie ma wartość bliską 1 to znaczy że jest typowo męskie a jeśli bliską 0 to imie jest typowo kobiece
    everything_1930['Popularity_1930'] = abs((everything_1930['male'] - everything_1930['female'])/everything_1930['all'])
    everything_1930 = everything_1930.sort_values(by='Popularity_1930', ascending=True)
    everything_2000['Popularity_2000'] = abs((everything_2000['male'] - everything_2000['female'])/everything_2000['all'])
    everything_2000 = everything_2000.sort_values(by='Popularity_2000', ascending=True)
    # print(everything_1930)
    # print(everything_2000)

    everything_1930 = everything_1930.drop(columns = ['male', 'all', 'female'])
    everything_2000 = everything_2000.drop(columns = ['male', 'all', 'female'])

    # Znajduje imiona które występują zarówno w latach do 1930 i po 2000. Jeśli wartość imienia jest wysoka to znaczy że zmiana występowania tego imienia jest duża
    everything = everything_1930.merge(everything_2000, left_on='name', right_on='name')
    everything['end'] = abs(everything['Popularity_2000'] - everything['Popularity_1930'])
    everything = everything.sort_values(by='end', ascending=False)
    print(everything)


    Name1_course = df_10.loc[lambda df_10: df_10['name'] == 'Sidney'] # wykreślam popularność tego imienia wśród mężczyzn i Kobiet
    Name1_course_M = Name1_course[lambda Name1_course: Name1_course['sex'] == 'M']
    Name1_course_F = Name1_course[lambda Name1_course: Name1_course['sex'] == 'F']
    Name1_course_F['count'] *= -1
    # print(Name1_course_M)
    # print(Name1_course_F)
    ax_Name1 = Name1_course_M.plot.bar(x = 'year', y = 'count', rot=0, color='b')
    Name1_course_F.plot.bar(x = 'year', y = 'count',rot=0, color='r', ax=ax_Name1)
    ax_Name1.tick_params(axis='x', labelrotation=90)
    plt.legend(['Male', 'Female'], loc='lower left', title='Legend')
    fig = pylab.gcf()
    fig.canvas.manager.set_window_title('Zad10 Name1 Sidney')



    Name2_course = df_10.loc[lambda df_10: df_10['name'] == 'Jessie']
    Name2_course_M = Name2_course[lambda Name2_course: Name2_course['sex'] == 'M']
    Name2_course_F = Name2_course[lambda Name2_course: Name2_course['sex'] == 'F']
    Name2_course_F['count'] *= -1
    ax_Name2 = Name2_course_M.plot.bar(x = 'year', y = 'count', rot=0, color='b')
    Name2_course_F.plot.bar(x = 'year', y = 'count',rot=0, color='r', ax=ax_Name2)
    ax_Name2.tick_params(axis='x', labelrotation=90)
    plt.legend(['Male', 'Female'], loc='lower left', title='Legend')
    fig = pylab.gcf()
    fig.canvas.manager.set_window_title('Zad10 Name2 Jessie')
    plt.show()



def zad11():

    conn = sqlite3.connect("demography_us.sqlite")  # połączenie do bazy danych - pliku
    c = conn.cursor()

    all = []
    for row in c.execute('SELECT population.Age, population.Year, population.Total FROM population WHERE population.Year BETWEEN 1935 AND 2020'):
        all.append(row)

    # print(all)
    conn.close()

def zad12():
    conn = sqlite3.connect("demography_us.sqlite")
    c1 = conn.cursor()
    c2 = conn.cursor()

    data_b = []
    data_d = []
    population = []
    birthrate_all = []

    for row in c1.execute('SELECT births.Total FROM births WHERE births.Year BETWEEN 1935 AND 2020'):
        data_b.append(row)
    for row in c2.execute('SELECT SUM(deaths.total) FROM deaths WHERE deaths.Year BETWEEN 1935 AND 2020 GROUP BY deaths.Year'):
        data_d.append(row)
    for row in c2.execute('SELECT sum(population.Total) FROM population WHERE population.Year BETWEEN 1935 AND 2020 GROUP BY population.Year'):
        population.append(row)

    # zminiam format tych plików i zapisuje je do list a następnie tworze liste z Przyrostem naturalnym
    for x in range(len(data_b)):
        data_b_f = float('.'.join(str(ele) for ele in data_b[x]))
        #print(data_b_f)
        data_d_f = float('.'.join(str(ele) for ele in data_d[x]))
        #print(data_d_f)
        population_f = float('.'.join(str(ele) for ele in population[x]))
        #print(population_f)
        birthrate = (data_b_f - data_d_f)*1000/population_f
        birthrate_all.append(birthrate)
        #print(birthrate)

    # print('Birthrate', birthrate_all)

    plt.plot(range(1936, 2022), birthrate_all)
    plt.title('Przyrost Naturalny')
    plt.ylabel('Współczynnik w %')
    fig = pylab.gcf()
    fig.canvas.manager.set_window_title('Zad12')

    plt.show()

    conn.close()

def zad13():

    conn = sqlite3.connect("demography_us.sqlite")  # połączenie do bazy danych - pliku
    c1 = conn.cursor()

    data_birth = []
    data_death = []
    survival_rate_table = []

    for row in c1.execute('SELECT births.Total FROM births'):
        data_birth.append(row)
    for row in c1.execute('SELECT deaths.total FROM deaths WHERE deaths.Age BETWEEN 0 AND 0 '):
        data_death.append(row)

    # Wykonuje je bardzo podobnie jak zad 12 ale tutaj od wartości dzieci które urodziły się w danym roku
    # odejmuje ilość dzieci które nie przeżyły roczka
    for x in range(len(data_birth)):
        data_birth_f = float('.'.join(str(ele) for ele in data_birth[x]))
        data_death_f = float('.'.join(str(ele) for ele in data_death[x]))
        survival_rate = (data_birth_f-data_death_f)/data_birth_f
        survival_rate_table.append(survival_rate*100)

    plt.plot(range(1934, 2022), survival_rate_table)
    plt.title('Współczynnik przeżywalności dzieci')
    plt.ylabel('Współczynnik w %')
    fig = pylab.gcf()
    fig.canvas.manager.set_window_title('Zad13')
    plt.show()

    conn.close()

def zad14():

    # z SQLITE wyznaczam ile mężczyzn i kobiet urodziło się w konkretnych latach,
    # tak samo robie z wcześniejszym zbiorem i następnie na wykreście pokazuje różnice w ilości urodzeń
    # u kobiet i facetów między tymi bazami danych
    conn = sqlite3.connect("demography_us.sqlite")
    c1 = conn.cursor()
    c2 = conn.cursor()

    data_birth_M = []
    data_birth_F = []
    data_birth_M_all = []
    data_birth_F_all = []

    for row in c1.execute('SELECT births.Male FROM births WHERE births.Year BETWEEN 1935 AND 2020'):
        data_birth_M.append(row)
    for row in c2.execute('SELECT births.Female FROM births WHERE births.Year BETWEEN 1935 AND 2020'):
        data_birth_F.append(row)



    for x in range(len(data_birth_M)):
        data_birth_M_all.append(float('.'.join(str(ele) for ele in data_birth_M[x])))
        data_birth_F_all.append(float('.'.join(str(ele) for ele in data_birth_F[x])))
    conn.close()

    df_14 = files_df

    df_1935_2021_M = df_14.loc[(df_14["sex"] == 'M')]
    df_1935_2021_M = df_1935_2021_M.loc[df_1935_2021_M['year'] > 1935]
    df_1935_2021_sum_Male = df_1935_2021_M.groupby(by = ['year']).sum()
    df_1935_2021_sum_Male = df_1935_2021_sum_Male.reset_index()
    df_1935_2021_sum_Male['sqlite'] = data_birth_M_all
    df_1935_2021_sum_Male['Diffrence_sqlite_pd'] = df_1935_2021_sum_Male['sqlite'] - df_1935_2021_sum_Male['count']
    # print(df_1935_2021_sum_Male)

    df_1935_2021_F = df_14.loc[(df_14["sex"] == 'F')]
    df_1935_2021_F = df_1935_2021_F.loc[df_1935_2021_F['year'] > 1935]
    df_1935_2021_sum_Female = df_1935_2021_F.groupby(by = ['year']).sum()
    df_1935_2021_sum_Female = df_1935_2021_sum_Female.reset_index()
    df_1935_2021_sum_Female['sqlite'] = data_birth_F_all
    df_1935_2021_sum_Female['Diffrence_sqlite_pd'] = df_1935_2021_sum_Female['sqlite'] - df_1935_2021_sum_Female['count']
    # print(df_1935_2021_sum_Female)


    fig, ax = plt.subplots()
    ax.plot(df_1935_2021_sum_Male['year'], df_1935_2021_sum_Male['Diffrence_sqlite_pd'], color='blue')
    ax.plot(df_1935_2021_sum_Female['year'], df_1935_2021_sum_Female['Diffrence_sqlite_pd'], color='red')

    min_diff_Male = abs(df_1935_2021_sum_Male['Diffrence_sqlite_pd']).min()
    max_diff_Male = abs(df_1935_2021_sum_Male['Diffrence_sqlite_pd']).max()
    year_min_diff_Male = df_1935_2021_sum_Male.loc[lambda df_1935_2021_sum_Male: df_1935_2021_sum_Male['Diffrence_sqlite_pd'] == min_diff_Male]
    year_max_diff_Male = df_1935_2021_sum_Male.loc[lambda df_1935_2021_sum_Male: df_1935_2021_sum_Male['Diffrence_sqlite_pd'] == max_diff_Male]
    year_min_diff_Male = year_min_diff_Male.drop(columns = ['count', 'sqlite'])
    year_max_diff_Male = year_max_diff_Male.drop(columns=['count', 'sqlite'])
    print('ZAD14:\nMin diffrence Male\n', year_min_diff_Male)
    print('\nMax diffrence Male\n', year_max_diff_Male)

    min_diff_Female = abs(df_1935_2021_sum_Female['Diffrence_sqlite_pd']).min()
    max_diff_Female = abs(df_1935_2021_sum_Female['Diffrence_sqlite_pd']).max()
    year_min_diff_Female = df_1935_2021_sum_Female.loc[lambda df_1935_2021_sum_Female: df_1935_2021_sum_Female['Diffrence_sqlite_pd'] == min_diff_Female]
    year_max_diff_Female = df_1935_2021_sum_Female.loc[lambda df_1935_2021_sum_Female: df_1935_2021_sum_Female['Diffrence_sqlite_pd'] == max_diff_Female]
    year_min_diff_Female = year_min_diff_Female.drop(columns = ['count', 'sqlite'])
    year_max_diff_Female = year_max_diff_Female.drop(columns=['count', 'sqlite'])
    print('\nMin diffrence Female\n', year_min_diff_Female)
    print('\nMax diffrence Female\n', year_max_diff_Female)

    fig = pylab.gcf()
    fig.canvas.manager.set_window_title('Zad14')
    plt.title('Różnica w ilości urodzeń mężczyzn i kobiet\nSqlite-Pandas')
    plt.legend(['Male','Female'], loc='lower right', title='Legend')
    plt.show()

if __name__ == '__main__':
    zad1() #Done
    zad2() #Done
    zad3() #Done
    zad4() #Done
    zad5() #Done
    zad6() #Done
    zad7() #Done
    zad8() #Done
    zad9() #Done
    zad10() #Done
    zad11() #Done
    zad12() #Done
    zad13() #Done
    zad14() #Done