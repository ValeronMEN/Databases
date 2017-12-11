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
    con = mdb.connect('localhost', 'root', '', 'guitars')
    with con:
        cur = con.cursor()
        cur.execute('%s%s' % ("SELECT * FROM ", table_name))
        rows = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        return merge_column_names_and_values(rows, field_names)


def get_text_column_names(table_name):
    con = mdb.connect('localhost', 'root', '', 'guitars')
    with con:
        cur = con.cursor()
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '%s' AND DATA_TYPE = 'TEXT'"
                    % table_name)
        rows = cur.fetchall()
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
    return


def clear_table(table_name):
    con = mdb.connect('localhost', 'root', '', 'guitars')
    with con:
        cur = con.cursor()
        cur.execute("TRUNCATE TABLE %s" % table_name)
    return


def clear_database():
    con = mdb.connect('localhost', 'root', '', 'guitars')
    with con:
        cur = con.cursor()
        cur.execute("SHOW TABLES")
        rows = cur.fetchall()
        for row in rows:
            clear_table(row[0])
    return


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
