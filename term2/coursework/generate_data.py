from connect_db import *
import random
import pandas as pd

SOURCE = [
    'ValeryBabenko-PC',
]

PERIOD = [
    '12 months',
]

YEAR = [
    2015,
    2016,
    2017,
]

QUARTER = [
    1,
    2,
    3,
    4,
]

LFSWEIGHT = [
    'pwt10',
]

GEOGRAPHY = [
    'Ukraine',
    'Columbia',
]

SEX = [
    'Male',
    'All adults',
    'Female',
]

AGE = [
    '75+',
    '16-24',
    '16+',
    '25-34',
    '35-44',
    '45-54',
    '55-64',
    '65-74',
]

CHARACTERISTIC = [
    'Children',
    'No children',
    'Owners',
    'Renters',
]


def read_table_column(tableName, columnName):
    conn = connect_db()
    cursor = conn.cursor()
    s = "SELECT %s FROM %s" % (columnName, tableName)
    cursor.execute(s)
    res = cursor.fetchall()
    listToReturn = []
    for elem in res:
        listToReturn.append(elem)
    return listToReturn


def read_table_all(tableName):
    list = read_table_column(tableName, "*")
    for el in list:
        print(el)


def read_characteristicvars_table_all():
    read_table_all("public.characteristicvars")


def read_measurementvars_table_all():
    read_table_all("public.measurementvars")


def filter_table(tableName, column, value):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM %s WHERE %s=$$%s$$" % (tableName, column, value))
    res = cursor.fetchall()
    for elem in res:
        print(elem)
    if(len(res) >= 1):
        return 0
    else:
        return 1


def filter_characteristicvars_table(column, value):
    filter_table("public.characteristicvars", column, value)


def filter_measurementvars_table(column, value):
    filter_table("public.measurementvars", column, value)


def filter_characteristicvars_table_by_name(value):
    return filter_characteristicvars_table("characteristicvar", value)


def filter_measurementvars_table_by_name(value):
    return filter_measurementvars_table("measurementvar", value)


def insert_demography_data(source, period, year, quarter, lfsweight, measurementvar, geography, householdtype, sex, age,
             characteristicvar, characteristic, estimate, standarderror, unweightedcount):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO public.demography(source, period, year, quarter, lfsweight, measurementvar, '
                   'geography, householdtype, sex, age, characteristicvar, characteristic, estimate, standarderror,'
                   ' unweightedcount) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                   (source, period, year, quarter, lfsweight, measurementvar, geography, householdtype, sex, age,
                    characteristicvar, characteristic, estimate, standarderror, unweightedcount))
    print("[%s, %s, %i, %i, %s, %s, %s, %s, %s, %s, %s, %s, %d, %d, %i]"
          % (source, period, year, quarter, lfsweight, measurementvar, geography, householdtype, sex, age,
             characteristicvar, characteristic, estimate, standarderror, unweightedcount))
    conn.commit()


def generate_data(count):
    mesurementList = read_table_column("public.measurementvars", "measurementvar")
    characteristicList = read_table_column("public.characteristicvars", "characteristicvar")
    for i in range(count):
        source = random.choice(SOURCE)
        age = random.choice(AGE)
        sex = random.choice(SEX)
        geography = random.choice(GEOGRAPHY)
        lfsweight = random.choice(LFSWEIGHT)
        quarter = random.choice(QUARTER)
        year = random.choice(YEAR)
        period = random.choice(PERIOD)
        source = random.choice(SOURCE)
        characteristic = random.choice(CHARACTERISTIC)
        characteristicvar = random.choice(characteristicList)[0]
        measurementvar = random.choice(mesurementList)[0]
        estimate = random.uniform(0,100) #0.000000001
        unweightedcount = random.randint(0,3000)
        standarderror = random.uniform(0,10) #0.000000001
        householdtype = None
        insert_demography_data(source, period, year, quarter, lfsweight, measurementvar, geography, householdtype, sex,
                               age, characteristicvar, characteristic, estimate, standarderror, unweightedcount)
    print("done")


def read_data_fast():
    demographyPath = "D:\\coursework_db\\demographyFix.csv"
    fill_one_table('demography', demographyPath)
    print("done")


def read_data_at_start():
    characteristicvarPath = "D:\\coursework_db\\characteristicvar.csv"
    measurementvarPath = "D:\\coursework_db\\measurementvar.csv"
    fill_one_table('characteristicvars', characteristicvarPath)
    fill_one_table('measurementvars', measurementvarPath)


def fill_one_table(tableName, tablePath):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("TRUNCATE %s;" % (tableName));
    cursor.execute("COPY %s FROM '%s' WITH (FORMAT csv, ENCODING 'windows-1251');" % (tableName, tablePath))
    conn.commit()


def truncate_one_table(tableName):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("TRUNCATE %s;" % (tableName));
    conn.commit()


def truncate_db():
    truncate_one_table('demography')
    print("done")