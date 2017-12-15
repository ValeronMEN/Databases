import xml.etree.cElementTree as et
from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
import datetime


def parse_xml_file():
    tree = get_xml_file()
    root = tree.getroot()
    input_database = {}
    for table in root:
        tbl = []
        for instance in table:
            instances = {}
            for element in instance:
                if element.text:
                    text = clip(element.text)
                else:
                    text = ''
                instances.update({element.tag: text})
            tbl.append(instances)
        input_database.update({table.tag: tbl})
    return input_database


def get_xml_file():
    path = 'input.xml'
    try:
        return et.ElementTree(file=path)
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
        for instance in table:
            guitar = SubElement(guitars, 'instance')
            for title, value in instance.items():
                element = SubElement(guitar, title)
                if type(value).__name__ == "long":
                    value = str(value)
                if type(value).__name__ == "datetime":
                    value = str(value)
                element.text = value
    return prettify(top)


def create_xml_file(output):
    output_file = open("output.xml", 'w')
    output_file.write(output)
    output_file.close()
    return


def transport_xml_data():
    output_file = open("output.xml", 'r')
    transport_data = output_file.read()
    output_file.close()
    input_file = open("input.xml", 'w')
    input_file.write(transport_data)
    input_file.close()
    return


def clip(string):
    left_n = 0
    length = len(string)
    right_n = length
    for character in range(length):
        if string[left_n] == ' ' or string[left_n] == '\n':
            left_n += 1
        if string[right_n-1] == ' ' or string[right_n-1] == '\n':
            right_n -= 1
    return string[left_n:right_n]
