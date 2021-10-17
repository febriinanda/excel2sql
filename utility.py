from datetime import datetime


def convert(data):
    return datetime.strptime(data, '%Y%m%d').strftime('%d-%b-%y')


def reverse(data, def_value):
    if int(data) == 0:
        return def_value

    data.zfill(8)
    return datetime.strptime(data, '%d%m%Y').strftime('%d-%b-%y')