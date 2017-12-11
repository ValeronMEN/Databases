import datetime


def date_check(date):
    birthday_date_array = date.split(' ')
    if len(birthday_date_array) == 3:
        year = int(birthday_date_array[0], 10)
        if 1900 <= year <= datetime.datetime.now().year:
            month = int(birthday_date_array[1], 10)
            if 0 <= month <= 12:
                day = int(birthday_date_array[2], 10)
                if 1 <= day <= 31:
                    return datetime.date(year, month, day)
    return None

