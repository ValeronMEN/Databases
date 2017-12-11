# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from . import db_connector
from . import xml_handler
import urllib
import datetime
from django.shortcuts import redirect
from django.utils.datastructures import MultiValueDictKeyError


def index(request):
    template = loader.get_template('index.html')
    # return render(request, 'index.html', {})
    return HttpResponse(template.render({}, request))


def output_xml(request):
    output_database = db_connector.get_database()
    xml_handler.create_xml_file(xml_handler.create_xml_template(output_database))
    return HttpResponse("<h1>Output success!</h1>")


def input_xml(request):
    input_database = xml_handler.parse_xml_file()
    db_connector.clear_database()
    db_connector.insert_all_tables(input_database)
    return HttpResponse("<h1>Input success!</h1>")


def transput_xml(request):
    xml_handler.transport_xml_data()
    return HttpResponse("<h1>Transput success!</h1>")


def guitars(request):
    return elements(request, 'guitars')


def customers(request):
    return elements(request, 'customers')


def shops(request):
    return elements(request, 'shops')


def bills(request):
    return elements(request, 'bills')


def elements(request, table_name):
    bills_enum = dict()
    if table_name == 'bills':
        bills_enum = db_connector.get_bills_foreign_key_values()
    template = loader.get_template('elements.html')
    if request.method == 'GET':
        request_tail = request.GET.urlencode()
        message = 'All elements'
        if request_tail:
            respond = elements_filter(table_name, request_tail)
            if respond:
                context = {
                    'elements': respond,
                    'message': "Simple filtration results",
                    'table_name': table_name,
                }
                return HttpResponse(template.render(context, request))
            message = 'Elements not found'
        context = {
            'elements': db_connector.get_table(table_name),
            'message': message,
            'table_name': table_name,
            'add_dict': bills_enum,
        }
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        attr_t = request.POST['attr_t']
        attr_w = request.POST['attr_w']
        text = request.POST['text']
        words = request.POST['words']
        print(words)
        text_columns_array = db_connector.get_text_column_names(table_name)
        result = []
        for column_name in text_columns_array:
            if attr_w == column_name and words != '':
                result = db_connector.get_table_filtered_text_words(table_name, attr_w, words.split(' '))
            elif attr_t == column_name and text != '':
                result = db_connector.get_table_filtered_text_phrase(table_name, attr_t, text)
            if len(result) != 0:
                context = {
                    'elements': result,
                    'message': 'Boolean mode filtration results',
                    'table_name': table_name,
                }
                return HttpResponse(template.render(context, request))
        context = {
            'elements': db_connector.get_table(table_name),
            'message': 'Elements not found',
            'table_name': table_name,
            'add_dict': bills_enum,
        }
        return HttpResponse(template.render(context, request))


def add_element(request):
    if request.method == 'POST':
        print(request.POST)
        try:
            bill_request = {
                'IDguitar': request.POST['IDguitar'],
                'IDshop': request.POST['IDshop'],
                'IDcustomer': request.POST['IDcustomer'],
                'price': request.POST['price'],
                'ID': request.POST['ID'],
                'purchaseDatetime': request.POST['purchaseDatetime']
            }
        except MultiValueDictKeyError:
            return redirect('/bills')
        try:
            if bill_request['ID'] != '':
                int(bill_request['ID'])
            if bill_request['purchaseDatetime'] == '':
                bill_request['purchaseDatetime'] = datetime.datetime.now()
            else:
                datetime.datetime.strptime(bill_request['purchaseDatetime'], '%Y-%m-%d')
            if int(bill_request['price']) >= 0 and int(bill_request['IDguitar']) >= 0 and int(
                    bill_request['IDshop']) >= 0 \
                    and int(bill_request['IDcustomer']) >= 0:
                db_connector.insert_bill(bill_request)
        except ValueError:
            print('ValueError')
    return redirect('/bills')


def elements_filter(table_name, request_tail):
    request_tail = urllib.unquote(request_tail).replace('+', ' ')
    # in sent URL we have to have as minimal 3 symbols (for example, v=1)
    if len(request_tail) > 3:
        request_body = request_tail.split('=')
        # without '=' symbol: 3 - 1 = 2
        if len(request_body) == 2:
            attribute = request_body[0]
            # in this 'try' block we check type of the first value, that was sent
            # then we choose 'between' for digit values or 'in' for string values
            try:
                numbers = request_body[1].split('%3A')
                int(numbers[0])
                # in 'between' case we have to define only two numbers (for example, BETWEEN 1 AND 2)
                if 1 <= len(numbers) <= 2:
                    return db_connector.get_table_filtered_number(table_name, attribute, numbers)
            except ValueError:
                # this is 'in' case
                return db_connector.get_table_filtered_str(table_name, attribute, request_body[1].split('%3A'))
            except IndexError:
                return None
    return None
