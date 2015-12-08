# -*- encoding: utf-8 -*-
from __future__ import unicode_literals


from opensearchsdk.utils import Constants
from opensearchsdk.service import BaseService
from opensearchsdk.service import ResultInfo
from opensearchsdk import log
from opensearchsdk import set_stream_logger
from opensearchsdk.config import Config

__author__ = 'barycenter'


class SuggestMgr(BaseService):

    BASE_URL = "/suggest"

    def __init__(self, client):
        BaseService.__init__(self)
        self.__client = client

        if Config.DEBUG:
            set_stream_logger()

    def _check_client(self):
        if not self.__client:
            self.invalid_client()

    def suggest(self, query, index_name, suggest_name, hit=5):
        """
        suggest method
        :param query: the text you want to search
        :param index_name: the app name you want to search
        :param suggest_name: the suggest rule's name
        :param hit: suggest number
        :return:
        """
        if not query:
            raise ValueError("invalid query")

        if not index_name:
            raise ValueError("invalid index name")

        if not suggest_name:
            raise ValueError("invalid suggest name")

        if type(hit) is not int or hit > 10 or hit < 1:
            raise ValueError("invalid hit, please set a integer between [1, 10]")

        log.debug("Suggest %s / %s" % (index_name, suggest_name))

        self._check_client()

        params = dict()
        params['query'] = query
        params['index_name'] = index_name
        params['suggest_name'] = suggest_name
        params['hit'] = str(hit)

        url = SuggestMgr.BASE_URL

        resp = self.__client.send_message(url, method='GET', params=params)
        resp_info = self.wrap_result(resp)

        return resp_info

    def wrap_result(self, response):

        if response.ok():
            resp_json = response.response_json()
            if 'errors' in resp_json and resp_json['errors']:
                result = SuggestResultInfo(Constants.RETURN_FAIL, resp_json['errors'][0].get("message"), resp_json)
            else:
                result = SuggestResultInfo(Constants.RETURN_SUCCESS, "success", resp_json)
        else:
            result = SuggestResultInfo(Constants.RETURN_FAIL, "suggest failed", None)

        return result


class SuggestResultInfo(ResultInfo):

    def __init__(self, status, msg, json_result=None):
        ResultInfo.__init__(self, status, msg, json_result)

        if self.status == Constants.RETURN_SUCCESS:
            self.__init_suggest()

    def __init_suggest(self):
        self.suggests = []

        for item in self.result.get("suggestions"):
            self.suggests.append(item.get("suggestion"))

    def suggestions(self):
        return self.suggests
