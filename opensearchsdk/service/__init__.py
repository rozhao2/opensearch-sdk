# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from opensearchsdk import set_stream_logger
from opensearchsdk.base import Base
from opensearchsdk.config import Config
from opensearchsdk.utils import Constants

__author__ = 'barycenter'


class BaseService(Base):
    """
    BaseService
    """

    def __init__(self):
        if Config.DEBUG:
            set_stream_logger()

    def invalid_client(self):
        raise AttributeError("you need assign a valid OpenSearchClient when initialization")

    def wrap_result(self, response):
        """
        encapsulate http response to service response
        """
        if not response:
            return None

        if not response.ok():
            status = Constants.RETURN_FAIL
            if response.response_code() != 200:
                msg = "HTTP response not 200 OK"
                return ResultInfo(status, msg, None, None)

        try:
            result = response.response_json()

            status = result["status"].upper()

            if status != Constants.RETURN_SUCCESS:
                msg = "%s/%s" % (result["errors"][0]["code"], result["errors"][0]["message"])
                return ResultInfo(status, msg, None)

            return ResultInfo(status, "", result)
        except ValueError:
            status = Constants.RETURN_FAIL
            msg = "no json response, please open debug log and check http response"
            return ResultInfo(status, msg, None, None)


class ResultInfo(Base):
    """
    API result
    """

    def __init__(self, status, msg, json_result=None):
        self.status = status
        self.msg = msg
        self.result = json_result

    def error_code(self):
        if self.result:
            if self.success():
                return "0000"
            else:
                return self.result["errors"][0]["code"]
        else:
            return -1

    def success(self):
        return self.status.upper() == Constants.RETURN_SUCCESS
