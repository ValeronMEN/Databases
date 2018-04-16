from django.template import loader
from django.http import HttpResponse
import MySQLdb as mdb
from guitarsapp.models import Customer, Shop, Guitar, Bill
import urllib, datetime
from . import db_connector


def elements(request, table_name):
    dropdown_values = dict()
    if table_name == 'guitarsapp_bill':
        dropdown_values = get_bills_foreign_key_values()
    template = loader.get_template('elements.html')
    if request.method == 'GET':
        return elements_get(request, table_name, template, dropdown_values)
    elif request.method == 'POST':
        return elements_post_filter(request, table_name, template, dropdown_values)


def elements_get(request, table_name, template, dropdown_values):
    request_tail = request.GET.urlencode()
    message = 'All elements'
    if request_tail:
        respond = elements_get_filter(table_name, request_tail)
        if respond:
            context = {
                'elements': respond,
                'message': "Simple filtration results",
                'table_name': table_name,
                'dropdown_values': dropdown_values,
                'event_time': get_reduce_event_time(),
                'trigger_switch': get_activate_button_label(),
            }
            return HttpResponse(template.render(context, request))
        message = 'Elements not found'
    context = {
        'elements': get_table_values_to_display(table_name),
        'message': message,
        'table_name': table_name,
        'dropdown_values': dropdown_values,
        'event_time': get_reduce_event_time(),
        'trigger_switch': get_activate_button_label(),
    }
    return HttpResponse(template.render(context, request))


def elements_get_filter(table_name, request_tail):
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
                numbers = request_body[1].split(':')
                int(numbers[0])
                # in 'between' case we have to define only two numbers (for example, BETWEEN 1 AND 2)
                if 1 <= len(numbers) <= 2:
                    return db_connector.get_table_filtered_number(table_name, attribute, numbers)
            except ValueError:
                # this is 'in' case
                return db_connector.get_table_filtered_str(table_name, attribute, request_body[1].split(':'))
            except IndexError:
                return None
    return None


def elements_post_filter(request, table_name, template, dropdown_values):
    attr_t = request.POST['attr_t']
    attr_w = request.POST['attr_w']
    text = request.POST['text']
    words = request.POST['words']
    text_columns_array = db_connector.get_text_column_names(table_name)
    print(text_columns_array)
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
                    'event_time': get_reduce_event_time(),
                    'trigger_switch': get_activate_button_label(),
                }
                return HttpResponse(template.render(context, request))
    context = {
        'elements': get_table_values_to_display(table_name),
        'message': 'Elements not found',
        'table_name': table_name,
        'dropdown_values': dropdown_values,
        'event_time': get_reduce_event_time(),
        'trigger_switch': get_activate_button_label(),
    }
    return HttpResponse(template.render(context, request))


def get_table_values_to_display(table_name):
    if table_name == 'guitarsapp_bill':
        bill_values = get_table_object(table_name).objects.all().values()
        for bill_value in bill_values:
            bill_value['guitar_type'] = Bill.objects.get(bill_id=bill_value['bill_id']).bill_guitar.type
            bill_value['guitar_name'] = Bill.objects.get(bill_id=bill_value['bill_id']).bill_guitar.name
            bill_value['guitar_brand'] = Bill.objects.get(bill_id=bill_value['bill_id']).bill_guitar.brand
            bill_value['guitar_color'] = Bill.objects.get(bill_id=bill_value['bill_id']).bill_guitar.color
            bill_value['guitar_producer'] = Bill.objects.get(bill_id=bill_value['bill_id']).bill_guitar.producer
            bill_value['guitar_description'] = Bill.objects.get(bill_id=bill_value['bill_id']).bill_guitar.description

            bill_value['customer_first_name'] = Bill.objects.get(bill_id=bill_value['bill_id']).bill_customer.first_name
            bill_value['customer_last_name'] = Bill.objects.get(bill_id=bill_value['bill_id']).bill_customer.last_name

            bill_value['shop_name'] = Bill.objects.get(bill_id=bill_value['bill_id']).bill_shop.shop_name
            bill_value['shop_type'] = Bill.objects.get(bill_id=bill_value['bill_id']).bill_shop.shop_type
            bill_value['shop_description'] = Bill.objects.get(bill_id=bill_value['bill_id']).bill_shop.shop_description
        return bill_values
    else:
        return get_table_object(table_name).objects.all().values()


def get_bills_foreign_key_values():
    guitars_obj = Guitar.objects.only('guitar_id')
    shops_obj = Shop.objects.only('shop_id')
    customers_obj = Customer.objects.only('customer_id')
    guitars_id = list()
    shops_id = list()
    customers_id = list()
    for guitar in guitars_obj:
        guitars_id.append(int(guitar.guitar_id))
    for shop in shops_obj:
        shops_id.append(int(shop.shop_id))
    for customer in customers_obj:
        customers_id.append(int(customer.customer_id))
    return {
        'bill_guitar_id': guitars_id,
        'bill_shop_id': shops_id,
        'bill_customer_id': customers_id,
    }


def get_activate_button_label():
    if not get_reduce_trigger():
        return 'Activate'
    else:
        return 'Deactivate'


def create_reduce_trigger():
    con = mdb.connect('localhost', 'root', '', 'guitars_new')
    with con:
        cur = con.cursor()
        cur.execute("CREATE TRIGGER `reduce_trigger` "
                    "BEFORE INSERT ON `guitarsapp_bill` "
                    "FOR EACH ROW BEGIN "
                    "SET NEW.price = NEW.price * 2; "
                    "END")


def get_reduce_trigger():
    con = mdb.connect('localhost', 'root', '', 'guitars_new')
    with con:
        cur = con.cursor()
        cur.execute("SHOW TRIGGERS")
        rows = cur.fetchall()
        return rows


def delete_reduce_trigger():
    con = mdb.connect('localhost', 'root', '', 'guitars_new')
    with con:
        cur = con.cursor()
        cur.execute("DROP TRIGGER reduce_trigger;")


def get_reduce_event_time():
    con = mdb.connect('localhost', 'root', '', 'guitars_new')
    with con:
        cur = con.cursor()
        cur.execute("SHOW events;")
        rows = cur.fetchall()
        result = rows[0][8]
        return result.ctime()


def get_table_object(table_name):
    if table_name == 'guitarsapp_shop':
        return Shop
    elif table_name == 'guitarsapp_customer':
        return Customer
    elif table_name == 'guitarsapp_guitar':
        return Guitar
    elif table_name == 'guitarsapp_bill':
        return Bill


def set_reduce_event_time(time):
    con = mdb.connect('localhost', 'root', '', 'guitars_new')
    with con:
        cur = con.cursor()
        cur.execute("ALTER EVENT reduce_event ON SCHEDULE EVERY 1 WEEK STARTS '%s' DO CALL reduce_price();"
                    % (time,))


def call_procedure():
    con = mdb.connect('localhost', 'root', '', 'guitars_new')
    with con:
        cur = con.cursor()
        cur.callproc('reduce_price')
