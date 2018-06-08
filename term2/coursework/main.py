from analys_data import *
from generate_data import *
from filter_data import *

def start():
    read_data_at_start()
    print("Hello, stranger! Welcome to COURSEWORK9000. Type 'help' to call the help menu. Enter the command:")
    while True:
        inputString = input(">> ").lower().replace(' ', '')
        if inputString == 'help':
            print("Available commands:\n"
                  "type 'help' to help\n"
                  "type 'read' to read the data from .csv files on the computer\n"
                  "type 'getc' to get all of the characteristicvar descriptions\n"
                  "type 'getm' to get all of the measurementvar descriptions\n"
                  "type 'generate' to generate some random data\n"
                  "type 'filter' to filter data\n"
                  "type 'analyse' to run the analyst functions\n"
                  "type 'truncate' to truncate the database tables\n"
                  "type 'exit' to exit")
        elif inputString == 'analyse':
            run_the_analysis()
        elif inputString == 'filter':
            filter_main()
        elif inputString == "read":
            read_data_fast()
        elif inputString == "generate":
            count = int(input("Enter the count\n>> "))
            generate_data(count)
        elif inputString == "truncate":
            truncate_db()
        elif inputString == 'getc':
            read_characteristicvars_table_all()
        elif inputString == 'getm':
            read_measurementvars_table_all()
        elif inputString == "exit":
            break


def filter_main():
    print(""" Filter by
                1 - sex
                2 - source
                3 - characteristic variable
                4 - measurement variable
                5 - age
                6 - estimate >
                7 - estimate <
                8 - standard error >
                9 - standard error <
                10 - unweighted count >
                11 - unweighted count <
                12 - quit
                """)

    filterString = int(input("Enter the number to filter by proposed criterium\n>> "))
    if filterString == 12:
        return
    elif filterString == 1:
        print("""
                    1 - Male 
                    2 - Female
                    3 - All adults
                    """)
        c = int((input("Enter the number\n>> ")))
        if c == 1:
            filter_by_sex("Male")
        elif c == 2:
            filter_by_sex("Female")
        elif c == 3:
            filter_by_sex("All adults")
        else:
            print("Error input")
    elif filterString == 2:
        c = input("Enter the source\n>> ")
        filter_source(c)
    elif filterString == 3:
        c = input("Enter the CharacteristicVar\n>> ")
        if (filter_characteristicvars_table_by_name(c) == 1):
            print("Error value")
        else:
            print("Entities from the demography table:")
            filter_by_charactheristicvar(c)
    elif filterString == 4:
        c = input("Enter the MeasurementVar\n>> ")
        if (filter_measurementvars_table_by_name(c) == 1):
            print("Error value")
        else:
            print("Entities from the demography table:")
            filter_by_measurementvar(c)
    elif filterString == 5:
        c = input("Enter the age bounds\n>> ")
        filter_by_age(c)
    elif filterString == 6:
        c = (input("Enter the estimate less than you want to see\n>> "))
        filter_by_estimate_gt(c)
    elif filterString == 7:
        c = (input("Enter the estimate greater than you want to see\n>> "))
        filter_by_estimate_lt(c)
    elif filterString == 8:
        c = (input("Enter the StandardError less than you want to see\n>> "))
        filter_by_standarderror_gt(c)
    elif filterString == 9:
        c = (input("Enter the StandardError greater than you want to see\n>> "))
        filter_by_standarderror_lt(c)
    elif filterString == 10:
        c = (input("Enter the unweighted count less than you want to see\n>> "))
        filter_by_unweightedcount_gt(c)
    elif filterString == 11:
        c = (input("Enter the unweighted count greater than you want to see\n>> "))
        filter_by_unweightedcount_lt(c)
    else:
        print("Error input")


start()
