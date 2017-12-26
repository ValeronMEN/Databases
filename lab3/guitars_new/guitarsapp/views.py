# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.shortcuts import redirect
from django.utils.datastructures import MultiValueDictKeyError
from . import db_connector, xml_handler, logick
import urllib, datetime
from guitarsapp.models import Customer, Shop, Guitar, Bill
import django.apps


def index(request):
    return HttpResponse(loader.get_template('index.html').render({}, request))


def output_xml(request):
    output_database = get_database()
    print(output_database)
    xml_handler.create_xml_file(xml_handler.create_xml_template(output_database))
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
    Bill.objects.all().delete()
    Customer.objects.all().delete()
    Guitar.objects.all().delete()
    Shop.objects.all().delete()
    # db_connector.insert_all_tables(input_database)
    return HttpResponse("<h1>Input XML success!</h1>")


def transport_xml(request):
    xml_handler.transport_xml_data()
    return HttpResponse("<h1>Transport XML success!</h1>")


def guitars(request):
    return logick.elements(request, 'guitarsapp_guitar')


def customers(request):
    return logick.elements(request, 'guitarsapp_customer')


def shops(request):
    return logick.elements(request, 'guitarsapp_shop')


def bills(request):
    return logick.elements(request, 'guitarsapp_bill')


def events(request):
    if request.method == 'POST':
        try:
            event_time = request.POST['event_time']
            day, month, year, hours, minutes, seconds = event_time.split('/')
            time = datetime.datetime(int(year), int(month), int(day), int(hours), int(minutes), int(seconds))
            logick.set_reduce_event_time(time)
        except IndexError:
            print('IndexError')
        except ValueError:
            print('ValueError')
    return redirect('/bills')


def triggers(request):
    if not logick.get_reduce_trigger():
        logick.create_reduce_trigger()
    else:
        logick.delete_reduce_trigger()
    return redirect('/bills')


def procedures(request):
    if request.method == 'POST':
        logick.call_procedure()
    return redirect('/bills')


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
            method = 'insert'
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
                if method == 'insert':
                    new_bill = Bill(bill_guitar_id=bill_request['bill_guitar_id'],
                                    bill_shop_id=bill_request['bill_shop_id'],
                                    bill_customer_id=bill_request['bill_customer_id'],
                                    price=bill_request['price'],
                                    purchase_datetime=bill_request['purchase_datetime'])
                    new_bill.save()
                elif method == 'update':
                    Bill.objects.filter(bill_id=bill_request['bill_id']).update(
                        bill_guitar_id=bill_request['bill_guitar_id'],
                        bill_shop_id=bill_request['bill_shop_id'],
                        bill_customer_id=bill_request['bill_customer_id'],
                        price=bill_request['price'],
                        purchase_datetime=bill_request['purchase_datetime'])
        except ValueError:
            print('ValueError')
    return redirect('/bills')


def delete_element(request):
    if request.method == 'POST':
        request_tail = request.path.split('/')
        table_name_url = 'bills'
        try:
            table_name = request_tail[2]
            element_id = request_tail[3]
            if table_name == 'guitarsapp_bill':
                Bill.objects.filter(bill_id=int(element_id)).delete()
                table_name_url = 'bills'
            elif table_name == 'guitarsapp_guitar':
                Guitar.objects.filter(guitar_id=int(element_id)).delete()
                table_name_url = 'guitars'
            elif table_name == 'guitarsapp_shop':
                Shop.objects.filter(shop_od=int(element_id)).delete()
                table_name_url = 'shops'
            elif table_name == 'guitarsapp_customer':
                Customer.objects.filter(customer_id=int(element_id)).delete()
                table_name_url = 'customers'
        except IndexError:
            return HttpResponse('<h1>INDEX ERROR</h1>')
        return redirect('/%s' % table_name_url)
    return HttpResponse('<h1>You need to use POST request in here</h1>')
