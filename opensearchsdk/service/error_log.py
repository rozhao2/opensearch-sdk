# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from opensearchsdk.service import BaseService
from opensearchsdk.service import ResultInfo
from opensearchsdk import log
from opensearchsdk import set_stream_logger
from opensearchsdk.utils import Constants
from opensearchsdk.config import Config

__author__ = 'barycenter'


class ErrorLog(BaseService):
    BASE_URL = "/index/error"

    def __init__(self, client):
        BaseService.__init__(self)
        self.__client = client

        if Config.DEBUG:
            set_stream_logger()

    def _check_client(self):
        if not self.__client:
            self.invalid_client()

    def get_log(self, app_name, page, page_size, sort_mod="DESC"):

        log.debug("get error log of %s" % (app_name))

        self._check_client()

        if not app_name:
            raise ValueError("app_name must be assigned")

        if type(page_size) is not int or page_size < 1:
            raise ValueError("invalid page_size, please set a integer bigger than 0")

        if page_size > 100:
            log.warning("page_size bigger than 100, this may not be a good idea")

        if type(page) is not int or page < 1:
            raise ValueError("invalid page, please set a integer bigger than 0")

        params = dict()
        params['page'] = str(page)
        params['page_size'] = str(page_size)
        params['sort_mode'] = sort_mod

        url = "%s/%s" % (ErrorLog.BASE_URL, app_name)

        resp = self.__client.send_message(url, method='GET', params=params)
        resp_info = self.wrap_result(resp)

        return resp_info

    def wrap_result(self, response):
        if response.ok():
            resp_json = response.response_json()
            if 'errors' in resp_json and resp_json['errors']:
                result = LogResultInfo(Constants.RETURN_FAIL, resp_json['errors'][0].get("message"), resp_json)
            else:
                result = LogResultInfo(Constants.RETURN_SUCCESS, "success", resp_json)
        else:
            result = LogResultInfo(Constants.RETURN_FAIL, "suggest failed", None)
        return result


class LogResultInfo(ResultInfo):
    """
    encapsulate Log ResultInfo
    """
    def __init__(self, status, msg, json_result=None):
        ResultInfo.__init__(self, status, msg, json_result=None)

        if status == Constants.RETURN_SUCCESS:
            self.logs = json_result["result"]["items"]

    def logs(self):
        return self.logs



