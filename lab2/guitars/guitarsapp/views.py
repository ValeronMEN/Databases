# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from . import db_connector
from . import xml_handler

# return HttpResponse("<h1>Hell yeah</h1>")
# return render(request, 'index.html', {})


def index(request):
    template = loader.get_template('index.html')
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
    request_tail = request.GET.urlencode()
    template = loader.get_template('elements.html')
    message = 'All elements'
    if request_tail:
        respond = elements_filter('guitars', request_tail)
        if respond:
            context = {
                'elements': respond,
                'message': "Filtered elements"
            }
            return HttpResponse(template.render(context, request))
        message = 'Elements not found'
    context = {
        'elements': db_connector.get_table('guitars'),
        'message': message
    }
    return HttpResponse(template.render(context, request))


def customers(request):
    template = loader.get_template('elements.html')
    context = {
        'elements': db_connector.get_table('customers'),
        'message': 'All elements'
    }
    return HttpResponse(template.render(context, request))


def elements_filter(table_name, request_tail):
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
