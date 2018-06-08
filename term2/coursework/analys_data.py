from connect_db import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates


PLOT_LABEL_FONT_SIZE = 8


def getColors(n):
    COLORS = []
    cm = plt.cm.get_cmap('hsv', n)
    for i in np.arange(n):
        COLORS.append(cm(i))
    return COLORS


def dict_sort_by_values(my_dict):
    keys = []
    values = []
    my_dict = sorted(my_dict.items(), key=lambda x:x[1], reverse=True)
    for k, v in my_dict:
        keys.append(k)
        values.append(v)
    return (keys,values)


def dict_sort_by_keys(my_dict):
    keys = []
    values = []
    my_dict = sorted(my_dict.items(), key=lambda x:x[0], reverse=True)
    for k, v in my_dict:
        keys.append(k)
        values.append(v)
    return (keys,values)


def get_keys_n_values(strEntities, strNumbers, strSqlFunc, isSort, isByValues):
    conn = connect_db()
    df = pd.read_sql(
        "SELECT {1}, {2}({0}) AS {0} FROM public.demography Group BY {1}".format(strEntities, strNumbers, strSqlFunc),
        conn)
    dict = {}
    for i in range(len(df.values)):
        dict[df.values[i][0]] = df.values[i][1]

    if (isSort):
        if(isByValues):
            dict_keys, dict_values = dict_sort_by_values(dict)
        else:
            dict_keys, dict_values = dict_sort_by_keys(dict)
    else:
        keys = []
        values = []
        for k, v in dict.items():
            keys.append(k)
            values.append(v)
        dict_keys, dict_values = keys, values
    return (dict_keys, dict_values)


def column_graph(title, yLabel, rot, strEntities, strNumbers, strSqlFunc, isSort, isByValues):
    dict_keys, dict_values = get_keys_n_values(strEntities, strNumbers, strSqlFunc, isSort, isByValues)

    top_keys = len(dict_keys)

    plt.title(title, fontsize=PLOT_LABEL_FONT_SIZE)
    plt.bar(np.arange(top_keys), dict_values, color=getColors(top_keys))
    plt.xticks(np.arange(top_keys), dict_keys, rotation=rot, fontsize=8)
    plt.yticks(fontsize=PLOT_LABEL_FONT_SIZE)
    plt.ylabel(yLabel, fontsize=PLOT_LABEL_FONT_SIZE)
    plt.show()


def run_the_analysis():
    column_graph("Середня оцінка кожного типу правопорушення",
                 "Estimate", 90, "estimate", "measurementvar", "AVG", True, True)
    column_graph("Середня похибка кожного типу правопорушення", "StandardError", 90, "standarderror",
                 "measurementvar", "AVG", True, True)
    column_graph("Кількість правопорушень у кожній віковій групі", "Crime count", 90, "age",
                 "age", "COUNT", False, True)
    column_graph("Кількість правопорушень у кожній країні", "Crime count", 90, "geography",
                 "geography", "COUNT", False, True)
    column_graph("Кількість правопорушень за кожен рік", "Crime count", 90, "year",
                 "year", "COUNT", False, True)
    column_graph("Кількість правопорушень, що були вчинені різними групами людей (Жінки, Чоловіки, Усі)",
                 "Crime count", 90, "sex",
                 "sex", "COUNT", False, True)
    column_graph("Максимальна оцінка кожного типу правопорушення", "Estimate", 90, "estimate", "measurementvar", "MAX",
                 True, True)
    cycle_graph("Процентне співвідношення середніх оцінок кожного типу правопорушення",
                "estimate", "measurementvar", "AVG", True, True)
    cycle_graph("Процентне співвідношення максимальних оцінок кожного типу правопорушення",
                "estimate", "measurementvar", "MAX", False, True)
    line_graph("Кількість правопорушень за кожен рік", "Crime count", "55", "year",
                 "year", "COUNT", True, False)


def cycle_graph(title, strEntities, strNumbers, strSqlFunc, isSort, isByValues):
    dict_keys, dict_values = get_keys_n_values(strEntities, strNumbers, strSqlFunc, isSort, isByValues)

    # cycle part
    dpi = 80
    fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
    mpl.rcParams.update({'font.size': 9})
    plt.title(title)
    xs = range(len(dict_keys))
    plt.pie(
        dict_values, autopct='%.1f', radius=1.1,
        explode=[0.15] + [0 for _ in range(len(dict_keys) - 1)])
    plt.legend(
        bbox_to_anchor=(-0.16, 0.45, 0.25, 0.25),
        loc='lower left', labels=dict_keys)
    plt.show()


def line_graph(title, xLabel, yLabel, strEntities, strNumbers, strSqlFunc, isSort, isByValues):
    dict_keys, dict_values = get_keys_n_values(strEntities, strNumbers, strSqlFunc, isSort, isByValues)

    dpi = 80
    fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
    mpl.rcParams.update({'font.size': 10})

    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)

    ax = plt.axes()
    ax.yaxis.grid(True)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_major_locator(mdates.YearLocator())

    print(dict_keys)
    print(dict_values)

    plt.plot(dict_keys, dict_values, linestyle='solid', label="Crimes")
    plt.legend(loc='upper left', frameon=False)
    plt.show()