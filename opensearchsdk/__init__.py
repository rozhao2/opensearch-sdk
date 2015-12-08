# -*- encoding: utf-8 -*-
import platform
import logging

__author__ = 'barycenter'

VERSION = '1.0.0'

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

UserAgent = "aliyun-opensearch-python-sdk /%s /%s %s/%s" % (
    VERSION,
    platform.python_version(),
    platform.system(),
    platform.release()
)

log = logging.getLogger("opensearch-sdk")

def get_version():
    return VERSION

def set_stream_logger(level=logging.DEBUG, format_string=None):
    log.handlers=[]

    if not format_string:
        format_string = "%(asctime)s %(name)s [%(levelname)s]:%(message)s"

    log.setLevel(level)
    fh = logging.StreamHandler()
    formatter = logging.Formatter(format_string)
    fh.setFormatter(formatter)
    log.addHandler(fh)
