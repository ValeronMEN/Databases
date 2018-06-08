from connect_db import *


def filter_data(column, value):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM public.demography WHERE %s=$$%s$$" % (column, value))
    res = cursor.fetchall()
    for elem in res:
        print(elem)


def filter_lt(column, value):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM public.demography WHERE %s<=%s" % (column, value))
    res = cursor.fetchall()
    for elem in res:
        print(elem)


def filter_gt(column, value):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM public.demography WHERE %s>=%s" % (column, value))
    res = cursor.fetchall()
    for elem in res:
        print(elem)


def filter_by_estimate_lt(value):
    filter_lt("estimate", value)


def filter_by_estimate_gt(value):
    filter_gt("estimate", value)


def filter_by_standarderror_lt(value):
    filter_lt("standarderror", value)


def filter_by_standarderror_gt(value):
    filter_gt("standarderror", value)


def filter_by_unweightedcount_lt(value):
    filter_lt("unweightedcount", value)


def filter_by_unweightedcount_gt(value):
    filter_gt("unweightedcount", value)


def filter_by_source(value):
    filter_data("source", value)


def filter_by_sex(value):
    filter_data("sex", value)


def filter_by_charactheristicvar(value):
    filter_data("characteristicvar", value)


def filter_by_measurementvar(value):
    filter_data("measurementvar", value)


def filter_by_age(value):
    filter_data("age", value)
