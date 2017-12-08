# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from . import dbconnector

# return HttpResponse("<h1>Hell yeah</h1>")
# return render(request, 'index.html', {})


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))


def output_xml(request):
    input_database = dbconnector.get_all_essences()
    dbconnector.create_xml_file(dbconnector.create_xml_template(input_database))
    return HttpResponse("<h1>Success!</h1>")


def input_xml(request):
    dbconnector.parse_xml_file()
    return HttpResponse("<h1>Success!</h1>")


def guitars(request):
    template = loader.get_template('guitars.html')
    context = {
        'guitars': dbconnector.get_all_table_essences('guitar')
    }
    return HttpResponse(template.render(context, request))

