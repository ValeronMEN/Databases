import MySQLdb as mdb


def merge_column_names_and_values(rows, field_names):
    output_list = []
    for row in rows:
        format_output = {}
        field_names_length = len(field_names)
        for i in range(field_names_length):
            new_output = {
                field_names[i]: row[i],
            }
            format_output.update(new_output)
        output_list.append(format_output)
    return output_list


def get_table(table_name):
    if table_name == 'bills':
        return get_table_bills()
    con = mdb.connect('localhost', 'root', '', 'guitars')
    with con:
        cur = con.cursor()
        cur.execute('%s%s' % ("SELECT * FROM ", table_name))
        rows = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        return merge_column_names_and_values(rows, field_names)


def get_table_bills():
    con = mdb.connect('localhost', 'root', '', 'guitars')
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM bills LEFT OUTER JOIN guitars ON bills.IDguitar=guitars.ID "
                    "LEFT OUTER JOIN customers ON bills.IDcustomer = customers.ID "
                    "LEFT OUTER JOIN shops ON bills.IDshop = shops.ID")
        # In here we redefine ID field several times due to some ID fields in our SELECT respond
        bills_with_problem_id = merge_column_names_and_values(cur.fetchall(), [i[0] for i in cur.description])
        cur.execute("SELECT ID FROM bills")
        rows = cur.fetchall()
        # Then we get ID field from the original bills table and redefine it again
        i = 0
        for pair in bills_with_problem_id:
            pair.update({
                'ID': rows[i][0],
            })
            i += 1
        # Here we have proper ID fields
        return bills_with_problem_id


def get_values_from_table(table_name, attribute):
    con = mdb.connect('localhost', 'root', '', 'guitars')
    with con:
        cur = con.cursor()
        cur.execute("SELECT %s FROM %s" % (attribute, table_name))
        rows = cur.fetchall()
        rows_shorted = list()
        for row in rows:
            rows_shorted.append(row[0])
        return rows_shorted


def insert_bill(input):
    con = mdb.connect('localhost', 'root', '', 'guitars')
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO bills(IDguitar, IDshop, IDcustomer, price, purchaseDatetime, ID) "
                    "VALUES('%s', '%s', '%s', '%s', '%s', '%s')" % (input['IDguitar'], input['IDshop'],
                                                                    input['IDcustomer'], input['price'],
                                                                    input['purchaseDatetime'], input['ID']))


def get_bills_foreign_key_values():
    return {
        'IDguitar': get_values_from_table('guitars', 'ID'),
        'IDshop': get_values_from_table('shops', 'ID'),
        'IDcustomer': get_values_from_table('customers', 'ID'),
    }


def get_text_column_names(table_name):
    con = mdb.connect('localhost', 'root', '', 'guitars')
    with con:
        cur = con.cursor()
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '%s' AND DATA_TYPE = 'TEXT'"
                    % table_name)
        rows = cur.fetchall()
        if len(rows) == 0:
            return tuple()
        return rows[0]


def get_database():
    con = mdb.connect('localhost', 'root', '', 'guitars')
    with con:
        cur = con.cursor()
        cur.execute("SHOW TABLES")
        rows = cur.fetchall()
        output_database = {}
        for row in rows:
            table = get_table(row[0])
            if len(table) != 0:
                output_database.update({row[0]: table})
    return output_database


def insert_table(table, table_name):
    con = mdb.connect('localhost', 'root', '', 'guitars')
    with con:
        cur = con.cursor()
        tags = ""
        for essence in table:
            values = ""
            n = 0
            nk = len(essence)
            if tags == "":
                for tag, value in essence.items():
                    values += "'" + str(value) + "'"
                    tags += tag
                    if nk - 1 > n:
                        values += ", "
                        tags += ", "
                    n = n + 1
            else:
                for tag, value in essence.items():
                    values += "'" + str(value) + "'"
                    if nk - 1 > n:
                        values += ", "
                    n = n + 1
            request = "INSERT INTO %s(%s) VALUES(%s);" % (table_name, tags, values)
            cur.execute(request)


def insert_all_tables(input_database):
    con = mdb.connect('localhost', 'root', '', 'guitars')
    with con:
        cur = con.cursor()
        for name, table in input_database.items():
            insert_table(table, name)
    create_bills_constraints()
    return


def clear_table(table_name):
    con = mdb.connect('localhost', 'root', '', 'guitars')
    with con:
        cur = con.cursor()
        cur.execute("TRUNCATE TABLE %s" % table_name)
    return


def clear_database():
    # I was so tired to make it for general case
    clear_bills_constraints()
    # continue
    con = mdb.connect('localhost', 'root', '', 'guitars')
    with con:
        cur = con.cursor()
        cur.execute("SHOW TABLES")
        rows = cur.fetchall()
        for row in rows:
            clear_table(row[0])
    return


def clear_bills_constraints():
    con = mdb.connect('localhost', 'root', '', 'guitars')
    with con:
        cur = con.cursor()
        # cur.execute("SET foreign_key_checks = 0")
        cur.execute("ALTER TABLE bills DROP FOREIGN KEY bills_ibfk_3")
        cur.execute("ALTER TABLE bills DROP FOREIGN KEY bills_ibfk_2")
        cur.execute("ALTER TABLE bills DROP FOREIGN KEY bills_ibfk_1")


def create_bills_constraints():
    con = mdb.connect('localhost', 'root', '', 'guitars')
    with con:
        cur = con.cursor()
        # cur.execute("SET foreign_key_checks = 1")
        cur.execute("ALTER TABLE bills ADD FOREIGN KEY (IDguitar) REFERENCES guitars(ID)")
        cur.execute("ALTER TABLE bills ADD FOREIGN KEY (IDcustomer) REFERENCES customers(ID)")
        cur.execute("ALTER TABLE bills ADD FOREIGN KEY (IDshop) REFERENCES shops(ID)")


def get_all_foreign_keys():
    fk_req = "SELECT RC.CONSTRAINT_NAME FK_Name, KF.TABLE_SCHEMA FK_Schema, KF.TABLE_NAME FK_Table, " \
             "KF.COLUMN_NAME FK_Column, RC.UNIQUE_CONSTRAINT_NAME PK_Name, KP.TABLE_SCHEMA PK_Schema, " \
             "KP.TABLE_NAME PK_Table, KP.COLUMN_NAME PK_Column, RC.MATCH_OPTION MatchOption, " \
             "RC.UPDATE_RULE UpdateRule, RC.DELETE_RULE DeleteRule " \
             "FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS RC " \
             "JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE KF ON RC.CONSTRAINT_NAME = KF.CONSTRAINT_NAME " \
             "JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE KP ON RC.UNIQUE_CONSTRAINT_NAME = KP.CONSTRAINT_NAME"
    con = mdb.connect('localhost', 'root', '', 'guitars')
    with con:
        cur = con.cursor()
        cur.execute(fk_req)
        rows = cur.fetchall()
        todelete = list()
        todelete.append(rows[0][2])
        for row in rows:
            for contained in todelete:
                if contained != row[2]:
                    todelete.append(row[2])
        return todelete


def get_table_filtered_str(table_name, attribute, values):
    con = mdb.connect('localhost', 'root', '', 'guitars')
    with con:
        cur = con.cursor()
        cur.execute("SHOW COLUMNS FROM %s" % table_name)
        column_names = cur.fetchall()
        for column_name in column_names:
            if attribute == column_name[0]:
                # check if user send string values to int field
                if column_name[1] == 'int(11)':
                    for value in values:
                        if not value.isdigit():
                            return None
                # create an sequence like "value1','value2','value3"
                str_arg = "','".join(values)
                cur.execute("SELECT * FROM %s WHERE %s IN ('%s')" % (table_name, attribute, str_arg))
                rows = cur.fetchall()
                field_names = [i[0] for i in cur.description]
                return merge_column_names_and_values(rows, field_names)
    return None


def get_table_filtered_number(table_name, attribute, numbers):
    con = mdb.connect('localhost', 'root', '', 'guitars')
    with con:
        cur = con.cursor()
        cur.execute("SHOW COLUMNS FROM %s" % table_name)
        column_names = cur.fetchall()
        for column_name in column_names:
            if attribute == column_name[0] and column_name[1] == 'int(11)':
                # int this 'try' block we check all of the values if they consist of digits
                try:
                    first_number = int(numbers[0])
                    # in this if-else structure we check how many values was sent in here
                    if len(numbers) == 1:
                        second_number = first_number
                    else:
                        second_number = int(numbers[1])
                    cur.execute("SELECT * FROM %s WHERE %s BETWEEN %s AND %s" % (table_name, attribute,
                                                                                 first_number, second_number))
                    return merge_column_names_and_values(cur.fetchall(), [i[0] for i in cur.description])
                except ValueError:
                    return None
    return None


def get_table_filtered_text_words(table_name, attribute, words_array):
    con = mdb.connect('localhost', 'root', '', 'guitars')
    with con:
        cur = con.cursor()
        cur.execute("SHOW COLUMNS FROM %s" % table_name)
        column_names = cur.fetchall()
        for column_name in column_names:
            if attribute == column_name[0] and column_name[1] == 'text':
                query_str = " +".join(words_array)
                request = """SELECT * FROM %s WHERE MATCH %s AGAINST ('+%s' IN BOOLEAN MODE)""" \
                          % (table_name, attribute, query_str)
                print(request)
                cur.execute(request)
                return merge_column_names_and_values(cur.fetchall(), [i[0] for i in cur.description])
    return None


def get_table_filtered_text_phrase(table_name, attribute, phrase):
    con = mdb.connect('localhost', 'root', '', 'guitars')
    with con:
        cur = con.cursor()
        cur.execute("SHOW COLUMNS FROM %s" % table_name)
        column_names = cur.fetchall()
        for column_name in column_names:
            if attribute == column_name[0] and column_name[1] == 'text':
                cur.execute("""SELECT * FROM %s WHERE MATCH %s AGAINST ('"%s"' IN BOOLEAN MODE)"""
                            % (table_name, attribute, phrase))
                return merge_column_names_and_values(cur.fetchall(), [i[0] for i in cur.description])
    return None
