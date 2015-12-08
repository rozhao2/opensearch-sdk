# -*- encoding: utf-8 -*-
from __future__ import unicode_literals


from opensearchsdk.service import BaseService
from opensearchsdk import set_stream_logger
from opensearchsdk.config import Config

__author__ = 'barycenter'


class ReferenceMgr(BaseService):
    """
    API document seems not completed
    """

    BASE_URL = "/index"

    def __init__(self, client):
        BaseService.__init__(self)
        self.__client = client

        if Config.DEBUG:
            set_stream_logger()

    def _check_client(self):
        if not self.__client:
            self.invalid_client()

    def create_task(self, app_name, is_import=False, table_names=[]):
        """
        create index task
        :param is_import:
        :param table_names:
        :return:
        """

        if not app_name:
            raise ValueError("invalid app name")

        self._check_client()

        params = dict()
        params['action'] = 'createtask'
        if is_import:
            params['operate'] = 'import'

        if table_names and type(table_names) is list:
            params['table_name'] = ",".join(table_names)

        url = "%s/%s" % (ReferenceMgr.BASE_URL, app_name)

        resp = self.__client.send_message(url, method='GET', params=params)
        resp_info = self.wrap_result(resp)

        return resp_info

