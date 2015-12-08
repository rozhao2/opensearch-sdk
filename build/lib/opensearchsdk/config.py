# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from opensearchsdk.base import Base

__author__ = 'barycenter'


class Config(Base):
    DEBUG = True

    DEFAULT_HTTP_TIMEOUT = 20

    UPLOAD_MAX_LENGTH = 2 * 1024 * 1024

    ZONE_CONFIG = {
        "hangzhou": {
            "external": "http://opensearch-cn-hangzhou.aliyuncs.com",
            "internal": "http://intranet.opensearch-cn-hangzhou.aliyuncs.com",
            "VPC": "http://vpc.opensearch-cn-hangzhou.aliyuncs.com"
        },
        "beijing": {
            "external": "http://opensearch-cn-beijing.aliyuncs.com",
            "internal": "http://intranet.opensearch-cn-beijing.aliyuncs.com",
            "VPC": "http://vpc.opensearch-cn-beijing.aliyuncs.com"
        },
        "qingdao": {
            "external": "http://opensearch-cn-qingdao.aliyuncs.com",
            "internal": "http://intranet.opensearch-cn-qingdao.aliyuncs.com",
            "VPC": "http://vpc.opensearch-cn-qingdao.aliyuncs.com"
        }
    }

    @staticmethod
    def get_zone_url(zone, url_type):

        urls = Config.ZONE_CONFIG.get(zone)

        if not urls:
            raise Exception("invalid zone, please select one from [%s]" % ",".join(Config.ZONE_CONFIG.keys()))

        url = urls.get(url_type)

        if not url:
            raise Exception("invalid url type, please select on from [%s]" % ",".join(urls.keys()))

        return url
