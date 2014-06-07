import datetime

__author__ = 'airead'


def get_datetime_from_string(datestr, date_format='%Y/%m/%d %H:%M:%S'):
    return datetime.datetime.strptime(datestr, date_format)


def get_string_from_datetime(dateobj, date_format='%Y/%m/%d %H:%M:%S'):
    return dateobj.strftime(date_format)


def datetime_type(datestr):
    return get_datetime_from_string(datestr)


def bool_type(val):
    return val.lower() == 'true'
