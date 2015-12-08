# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from opensearchsdk.service import BaseService
from opensearchsdk import log
from opensearchsdk import set_stream_logger
from opensearchsdk.config import Config

__author__ = 'barycenter'


class ApplicationMgr(BaseService):

    BASE_URL = "/index"

    def __init__(self, client):
        BaseService.__init__(self)
        self.__client = client

        if Config.DEBUG:
            set_stream_logger()

    def _check_client(self):
        if not self.__client:
            self.invalid_client()

    def create(self, app_name, template_name="default"):
        """
        create an application according to template name
        :param template_name: template's name, you could pick up one from Constants
        :return: success, application's name; fail, error code
        """

        log.debug("Create Application %s / %s" % (app_name, template_name))

        self._check_client()

        params = dict()
        params['action'] = 'create'
        params['template'] = template_name

        url = "%s/%s" % (ApplicationMgr.BASE_URL, app_name)

        resp = self.__client.send_message(url, method='GET', params=params)
        resp_info = self.wrap_result(resp)

        return resp_info

    def delete(self, app_name):
        """
        delete an application by application name
        :param app_name: application's name
        :return:
        """

        log.debug("Delete Application %s" % app_name)

        self._check_client()

        params = dict()
        params['action'] = 'delete'

        url = "%s/%s" % (ApplicationMgr.BASE_URL, app_name)

        resp = self.__client.send_message(url, method='GET', params=params)
        resp_info = self.wrap_result(resp)

        return resp_info

    def view(self, app_name):
        """
        show an application's information by application name
        :param app_name: application's name
        :return:
        """
        log.debug("View Application %s" % app_name)

        self._check_client()

        params = dict()
        params['action'] = 'status'

        url = "%s/%s" % (ApplicationMgr.BASE_URL, app_name)

        resp = self.__client.send_message(url, method='GET', params=params)
        resp_info = self.wrap_result(resp)

        return resp_info

    def list(self, page, page_size):
        """
        get applications' list
        :return:
        """
        log.debug("View Application %s" % app_name)

        self._check_client()

        params = dict()
        params['page'] = page
        params['page_size'] = page_size

        url = "%s/%s" % (ApplicationMgr.BASE_URL, app_name)

        resp = self.__client.send_message(url, method='GET', params=params)
        resp_info = self.wrap_result(resp)

        return resp_info

