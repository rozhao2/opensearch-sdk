# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import time
import string
import random
import sys
import uuid
import six

__author__ = 'barycenter'


class Constants:
    def __init__(self):
        pass

    TIME_FORMAT_COMMON = "%Y%m%d%H%M%S"
    TIME_FORMAT_UTC = "%Y-%m-%dT%H:%M:%SZ"

    DEFAULT_ENCODE = "utf-8"

    RETURN_SUCCESS = "OK"
    RETURN_FAIL = "FAIL"

ERROR_CODE = {
    1000: "internal error, please retry or check syntax",
    1001: "no template find",
    1003: "unsupported index type",
    1004: "service unavailable temporarily",

    2001: "application not exists",
    2002: "application name has been existed",
    2003: "application number exceeded",
    2004: "invalid application name",
    2005: "application name required",
    2006: "no new application name",
    2007: "remark cannot be more than 300 words",
}

# end class Constants


def get_datetime_str(expect_format=Constants.TIME_FORMAT_COMMON):
    return time.strftime(expect_format, time.gmtime())


# ####random string#######
def get_random_str(length=32, sample_characters=string.ascii_letters + string.digits):
    result = "".join(map(lambda x: sample_characters[x],
                         [random.randint(0, len(sample_characters) - 1) for x in range(0, length)]))
    return result


def get_random_timestamp(length=17):
    if length <= 13:
        return str(time.time())
    else:
        return str(time.time()) + get_random_str(length - 13, string.digits)


def get_uuid():
    """
    :return: uuid1
    """
    return str(uuid.uuid1()).replace("-","")


# #### encode ######

def url_encode(data):
    if not data:
        return ""
    try:
        if sys.version[0] < 3:
            return data
        else:
            return data.enode(Constants.DEFAULT_ENCODE)
    except UnicodeDecodeError:
        return data


def common_encode(data):
    if not data:
        return ""

    try:
        if sys.version[0] < 3:
            return unicode(data).encode(Constants.DEFAULT_ENCODE)
        else:
            return data
    except UnicodeDecodeError:
        return data


def unicode_compat(klass):
    if not six.PY3:
        klass.__unicode__ = klass.__str__
        klass.__str__ = lambda self: self.__unicode__().encode(Constants.DEFAULT_ENCODE)
    return klass

