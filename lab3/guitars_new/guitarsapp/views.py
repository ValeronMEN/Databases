# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.datastructures import MultiValueDictKeyError
from . import db_connector
from . import xml_handler
import urllib
import datetime
from guitarsapp.models import Customer, Shop, Guitar, Bill
import django.apps


# django.apps.apps.get_models(include_auto_created=False, include_swapped=False)


def index(request):
    return HttpResponse(loader.get_template('index.html').render({}, request))


def output_xml(request):
    output_database = get_database()
    print(output_database)
    # xml_handler.create_xml_file(xml_handler.create_xml_template(output_database))
    return HttpResponse("<h1>Output XML success!</h1>")


def get_database():
    return {
        'guitars': Guitar.objects.all().values(),
        'shops': Shop.objects.all().values(),
        'customers': Customer.objects.all().values(),
        'bills': Bill.objects.all().values(),
    }


def input_xml(request):
    input_database = xml_handler.parse_xml_file()
    db_connector.clear_database()
    db_connector.insert_all_tables(input_database)
    return HttpResponse("<h1>Input XML success!</h1>")


def transport_xml(request):
    xml_handler.transport_xml_data()
    return HttpResponse("<h1>Transport XML success!</h1>")


def guitars(request):
    return elements(request, 'guitars')


def customers(request):
    return elements(request, 'customers')


def shops(request):
    return elements(request, 'shops')


def bills(request):
    return elements(request, 'bills')


def elements(request, table_name):
    dropdown_values = dict()
    if table_name == 'bills':
        dropdown_values = get_bills_foreign_key_values()
    template = loader.get_template('elements.html')
    if request.method == 'GET':
        request_tail = request.GET.urlencode()
        message = 'All elements'
        if request_tail:
            respond = elements_filter_get(table_name, request_tail)
            if respond:
                context = {
                    'elements': respond,
                    'message': "Simple filtration results",
                    'table_name': table_name,
                    'dropdown_values': dropdown_values,
                }
                return HttpResponse(template.render(context, request))
            message = 'Elements not found'
        context = {
            'elements': get_table_values_to_display(table_name),
            'message': message,
            'table_name': table_name,
            'dropdown_values': dropdown_values,
        }
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        return elements_filter_post(request, table_name, template, dropdown_values)


def get_table_values_to_display(table_name):
    if table_name == 'bills':
        print(get_table_object(table_name).objects.all().select_related().values())
        return get_table_object(table_name).objects.all().select_related().values()
    else:
        return get_table_object(table_name).objects.all().values()


def get_bills_foreign_key_values():
    return {
        'bill_guitar_id': Guitar.objects.values('guitar_id'),
        'bill_shop_id': Shop.objects.values('shop_id'),
        'bill_customer_id': Customer.objects.values('customer_id'),
    }


def get_table_object(table_name):
    if table_name == 'shops':
        return Shop
    elif table_name == 'customers':
        return Customer
    elif table_name == 'guitars':
        return Guitar
    elif table_name == 'bills':
        return Bill


def add_bill(request):
    if request.method == 'POST':
        try:
            bill_request = {
                'bill_guitar_id': request.POST['bill_guitar_id'],
                'bill_shop_id': request.POST['bill_shop_id'],
                'bill_customer_id': request.POST['bill_customer_id'],
                'price': request.POST['price'],
                'bill_id': request.POST['bill_id'],
                'purchase_datetime': request.POST['purchase_datetime']
            }
        except MultiValueDictKeyError:
            return redirect('/bills')
        try:
            method = 'add'
            if bill_request['bill_id'] != '':
                user_bill_id = int(bill_request['bill_id'])
                existed_bill_ids = Bill.objects.values('bill_id')
                for existed_bill_id in existed_bill_ids:
                    if existed_bill_id == user_bill_id:
                        method = 'update'
                        break
            if bill_request['purchase_datetime'] == '':
                bill_request['purchase_datetime'] = datetime.datetime.now()
            else:
                datetime.datetime.strptime(bill_request['purchase_datetime'], '%Y-%m-%d')
            if int(bill_request['price']) >= 0 and int(bill_request['bill_guitar_id']) >= 0 and int(
                    bill_request['bill_shop_id']) >= 0 \
                    and int(bill_request['bill_customer_id']) >= 0:
                if method == 'add':
                    db_connector.insert_bill(bill_request)
                elif method == 'update':
                    db_connector.update_bill(bill_request)
        except ValueError:
            print('ValueError')
    return redirect('/bills')


def elements_filter_get(table_name, request_tail):
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


def elements_filter_post(request, table_name, template, dropdown_values):
    attr_t = request.POST['attr_t']
    attr_w = request.POST['attr_w']
    text = request.POST['text']
    words = request.POST['words']
    text_columns_array = db_connector.get_text_column_names(table_name)
    if len(text_columns_array) != 0:
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
                    'dropdown_values': dropdown_values,
                }
                return HttpResponse(template.render(context, request))
    context = {
        'elements': get_table_values_to_display(table_name),
        'message': 'Elements not found',
        'table_name': table_name,
        'dropdown_values': dropdown_values,
    }
    return HttpResponse(template.render(context, request))


def delete_bill(request):
    if request.method == 'POST':
        request_tail = request.path.split('/')
        try:
            table_name = request_tail[2]
            element_id = request_tail[3]
            db_connector.delete_record(table_name, 'bill_id', int(element_id))
        except IndexError:
            return HttpResponse('<h1>INDEX ERROR</h1>')
        return redirect('/%s' % request_tail[2])
    return HttpResponse('<h1>You need to use POST request in here</h1>')
