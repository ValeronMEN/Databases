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
    if request_tail:
        respond = guitars_filter('guitars', request_tail)
        if respond:
            template = loader.get_template('guitars.html')
            context = {
                'guitars': respond
            }
            return HttpResponse(template.render(context, request))
    template = loader.get_template('guitars.html')
    context = {
        'guitars': db_connector.get_table('guitars')
    }
    return HttpResponse(template.render(context, request))


def customers(request):
    template = loader.get_template('guitars.html')
    context = {
        'guitars': db_connector.get_table('customers')
    }
    return HttpResponse(template.render(context, request))


def guitars_filter(table_name, request_tail):
    if len(request_tail) > 3:
        request_body = request_tail.split('=')
        if len(request_body) == 2:
            attribute = request_body[0]
            try:
                int(request_body[1][0])
                numbers = request_body[1].split('%3A')
                if len(numbers) == 2:
                    return db_connector.get_table_filtered_number(table_name, attribute, numbers[0], numbers[1])
            except ValueError:
                values = "','".join(request_body[1].split('%3A'))
                return db_connector.get_table_filtered_str(table_name, attribute, values)
    return None
