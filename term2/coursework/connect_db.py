import psycopg2


def connect_db():
    try:
        conn = psycopg2.connect("dbname='crimes' user='postgres' host='localhost' password='1111'")
        return conn
    except:
        print("I am unable to connect to the database")