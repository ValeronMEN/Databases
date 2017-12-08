import MySQLdb as mdb
import xml.etree.cElementTree as ET
import os

from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement


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


def get_all_table_essences(table_name):
    con = mdb.connect('localhost', 'root', '', 'guitars')
    with con:
        cur = con.cursor()
        cur.execute('%s%s' % ("SELECT * FROM ", table_name))
        rows = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        return merge_column_names_and_values(rows, field_names)


def get_all_essences():
    con = mdb.connect('localhost', 'root', '', 'guitars')
    with con:
        cur = con.cursor()
        cur.execute("SHOW TABLES")
        rows = cur.fetchall()
        output_database = {}
        for row in rows:
            table = get_all_table_essences(row[0])
            if (len(table) != 0):
                output_database.update({row[0]: table})
    return output_database


def parse_xml_file():
    tree = get_xml_file()
    root = tree.getroot()
    input_database = {}
    for table in root:
        for essence in table:
            es = []
            for element in essence:
                es.append({element.tag: element.text.replace(' ', '').replace('\n', '')})
            input_database.update({table.tag: es})
    return input_database


def get_xml_file():
    path = 'input.xml'
    try:
        return ET.ElementTree(file=path)
    except IOError as e:
        print('nERROR - cant find file: %sn' % e)
    return


def prettify(elem):
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def create_xml_template(input_database):
    # input = {'guitars': [{'name': 'hhh', 'brand': 'bbb'}]}
    top = Element('guitar_shop')
    for name, table in input_database.items():
        guitars = SubElement(top, name)
        for essence in table:
            guitar = SubElement(guitars, 'essence')
            for title, value in essence.items():
                element = SubElement(guitar, title)
                if type(value).__name__ != "str":
                    value = str(value)
                element.text = value
    return prettify(top)


def create_xml_file(output):
    my_file = open("output.xml", 'w')
    my_file.write(output)
    my_file.close()
    return
