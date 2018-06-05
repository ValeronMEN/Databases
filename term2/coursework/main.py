from analys_data import *
from generate_data import *
from filter_data import *

def start():
    flag_main = True
    read_data_at_start()
    print("Hello, stranger! Welcome to COURSEWORK9000. Type 'help' to call the help menu. Enter the command:")
    while flag_main:
        inputString = input(">> ").lower().replace(' ', '')
        if inputString == 'help':
            print("Available commands:\n"
                  "type 'help' to help\n"
                  "type 'read' to read the data from .csv files on the computer\n"
                  "type 'generate' to generate some random data\n"
                  "type 'filter' to filter data\n"
                  "type 'analyse' to run the analyst functions\n"
                  "type 'truncate' to truncate the database tables\n"
                  "type 'exit' to exit")
        elif inputString == 'analyse':
            candidates_votes()
            party_votes()
            candidate_votes_democrat()
            candidate_votes_republican()
            state_votes_democrat()
            state_votes_republican()
        elif inputString == 'filter':
            print(""" Filter
            1 - party
            2 - state
            3 - state_abbr
            4 - candidate
            5 - votes >
            6 - votes <
            7 - quit
            """)

            b = int(input("Enter the command:"))
            if b == 7:
                break
            if b == 1:
                print("""1 - Republican 2 - Democrat""")
                c = int((input("Enter command:")))
                if c == 1:
                    filter_party("Republican")
                if c == 2:
                    filter_party("Democrat")
            if b == 2:
                c = input("Enter state:")
                filter_state(c)
            if b == 3:
                c = input("Enter st_abbr:")
                filter_st_abbr(c)
            if b == 4:
                c = input("Enter candidate:")
                filter_candidate(c)
            if b == 5:
                c = int(input("Enter gt votes:"))
                filter_votes_gt(c)
            if b == 6:
                c = int(input("Enter ls votes:"))
                filter_votes_ls(c)

            if (b < 1 or b > 7):
                print("Error number")
                flag_main = True

        elif inputString == "read":
            read_data_fast()
        elif inputString == "generate":
            count = int(input("Enter the count\n>> "))
            generate_data(count)
        elif inputString == "truncate":
            truncate_db()
        elif inputString == "exit":
            break

start()
