# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import json
import time

from opensearchsdk.service import BaseService
from opensearchsdk import log
from opensearchsdk import set_stream_logger
from opensearchsdk.config import Config

__author__ = 'barycenter'

class DataMgr(BaseService):
    """
    data operations
    """
    BASE_URL = "/index/doc"

    def __init__(self, client):
        BaseService.__init__(self)
        self.__client = client

        if Config.DEBUG:
            set_stream_logger()

    def _check_client(self):
        if not self.__client:
            self.invalid_client()

    def upload(self, app_name, table_name, items, retries=3, wait_time=1):
        """
        upload doc, if items is a json string, it will be uploaded， else it will raise
        a error
        if the item's length exceed 2M, it will not be uploaded
        if server returns 3007, it will retry 3 times (including the first time), retry times could be modified.
        it will wait 1 second between 2 retries

        sdk cannot assure users multi thread, so, sdk api doesn't query error log to

        :param app_name:  application name
        :param table_name: table name
        :param items: json string
        :param retries: retry times
        :return:
        """

        try:
            item_length = len(items)
            if item_length > Config.UPLOAD_MAX_LENGTH:
                log.error("items length %s cannot be more than %s" % (item_length, Config.UPLOAD_MAX_LENGTH))
        except TypeError:
            log.error("invalid json string when upload, please check param: items")
            return None

        try:
            json.dumps(items)
        except ValueError:
            log.error("invalid json string when upload")
            return None

        log.debug("Upload data %s / %s / %s" % (app_name, table_name, items))

        self._check_client()

        params = dict()
        params['action'] = 'push'
        params['table_name'] = table_name
        params['items'] = items

        url = "%s/%s" % (DataMgr.BASE_URL, app_name)

        retry = 0
        resp_info = None
        while retry < retries:
            retry += 1
            resp = self.__client.send_message(url, method='POST', params=params)
            resp_info = self.wrap_result(resp)
            if resp_info.success():
                break
            else:
                if resp_info.error_code() == "3007":
                    time.sleep(wait_time)
                    continue
                else:
                    log.error("upload failed, but the error code is not 3007, please check debug log")
                    break

        return resp_info
