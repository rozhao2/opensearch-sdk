# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from opensearchsdk.service import BaseService
from opensearchsdk.base import Base
from opensearchsdk import log
from opensearchsdk import set_stream_logger
from opensearchsdk.config import Config

__author__ = 'barycenter'


def lazy_prop(fn):
    """
    lazy load for query
    :param fn:
    :return:
    """
    attr_name = '_lazy_' + fn.__name__

    @property
    def _lazyprop(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazyprop

class Q(Base):
    """
    search condition, it could be organized complex query string
    for examle:
      Q(title="1"), Q(title="2") means query=title:"1" AND title:"2"
      Q(title="1"), Q(body="2")|Q(body="3") means query=title:"1" AND (body="2" OR body:"3")
      ～Q(tilte="1") means ANDNOT title:"1"
    """
    def __init__(self, *args, **kwargs):

        boost = None

        # only support the first one
        if len(args) > 0:
            tmp = args[0]
            if ":" not in tmp:
                log.warning("there is no index, it will be set default index")
                self.query_string = "default:'%s'" % tmp
            else:
                self.query_string = tmp
        elif len(kwargs) > 0:
            boost = kwargs.get('boost')
            if boost is not None:
                kwargs.pop('boost')

            if len(kwargs) == 0:
                raise ValueError("cannot only assign a boost parameter")

            self.query_string = "%s:'%s'" % (kwargs.items()[0][0], kwargs.items()[0][1])

        if boost is not None:
            self.query_string = "%s^%s" % (self.query_string, boost)

    def __or__(self, other):
        if other:
            if type(other) is not Q:
                raise TypeError("please use Q instance")
            query_string = "(%s OR %s)" % (self.query_string, other.query_string)
            q = Q()
            q.query_string = query_string
        else:
            raise TypeError("invalid operate")
        return q

    def __invert__(self):
        query_string = "ANDNOT %s" % self.query_string
        q = Q()
        q.query_string = query_string
        return q

    def __and__(self, other):
        if other:
            if type(other) is not Q:
                raise TypeError("please use Q instance")
            query_string = "(%s AND %s)" % (self.query_string, other.query_string)
        else:
            raise TypeError("invalid operate")
        q = Q()
        q.query_string = query_string
        return q

    def __pos__(self):
        """
        support + for sort sub search
        """
        query_string = "+%s" % self.query_string
        q = Q()
        q.query_string = query_string
        return q

    def __neg__(self):
        """
        support - for sub search
        """
        query_string = "-%s" % self.query_string
        q = Q()
        q.query_string = query_string
        return q

    def __repr__(self):
        return self.query_string

    def __str__(self):
        return self.__repr__()


class FQ(Base):
    """
    filter condition
    """

    def __init__(self, *args):
        if len(args) > 0:
            tmp = args[0]
            self.query_string = "'%s'" % tmp

    def __and__(self, other):
        if other:
            if type(other) is not FQ:
                raise TypeError("please use FQ instance")
            query_string = "(%s AND %s)" % (self.query_string, other.query_string)
        else:
            raise TypeError("invalid operate")
        q = FQ()
        q.query_string = query_string
        return q

    def __or__(self, other):
        if other:
            if type(other) is not FQ:
                raise TypeError("please use FQ instance")
            query_string = "(%s OR %s)" % (self.query_string, other.query_string)
        else:
            raise TypeError("invalid operate")
        q = FQ()
        q.query_string = query_string
        return q

    def __repr__(self):
        return self.query_string

    def __str__(self):
        return self.__repr__()


class Search(BaseService):
    """
    do opensearch operation
    WARNING: this class is NOT thread safe
    """

    BASE_URL = "/search"

    def __init__(self, client):
        BaseService.__init__(self)
        self.__client = client

        self.query_string = ""
        self.sub_searches = []

        self.__index_name = None
        self.__fetch_fields = None
        self.__qp = None
        self.__disable = None
        self.__first_formula_name = None
        self.__formula_name = None
        self.__summary = dict()

        self.__query = None
        self.__rank = None
        self.__sort = None
        self.__config = dict()
        self.__aggregate = None
        self.__filter = None
        self.__distinct = dict()
        self.__kvpairs = None

        if Config.DEBUG:
            set_stream_logger()

    def _check_client(self):
        if not self.__client:
            self.invalid_client()

    def index_name(self, *args):
        """
        pass application name you want to search, it support multiple application names
        :param args:
        :return:
        """
        self.__index_name = ";".join(args)
        return self

    def fetch_fields(self, *args):
        self.__fetch_fields = ";".join(args)
        return self

    def qp(self, *args):
        self.__qp = ";".join(args)
        return self

    def disable(self):
        self.__disable = 'qp'
        return self

    def first_formula_name(self, param):
        self.__first_formula_name = param
        return self

    def formula_name(self, param):
        self.__formula_name = param
        return self

    def summary(self, summary_field, summary_element=None, summary_ellipsis=None, summary_snipped=None,
                summary_len=None, summary_prefix=None, summary_postfix=None):

        if not summary_field:
            raise ValueError("please set summary_field when using summary")

        self.__summary['summary_field'] = summary_field

        if 'summary_element' not in self.__summary or self.__summary['summary_element'] != summary_element:
            self.__summary['summary_element'] = summary_element

        if 'summary_ellipsis' not in self.__summary or self.__summary['summary_ellipsis'] != summary_ellipsis:
            self.__summary['summary_ellipsis'] = summary_ellipsis

        if 'summary_snipped' not in self.__summary or self.__summary['summary_snipped'] != summary_snipped:
            self.__summary['summary_snipped'] = summary_snipped

        if 'summary_len' not in self.__summary or self.__summary['summary_len'] != summary_len:
            self.__summary['summary_len'] = summary_len

        if summary_prefix is None and summary_postfix is not None:
            raise ValueError("summary_prefix and summary_postfix should be provided both")

        if summary_prefix is not None and summary_postfix is None:
            raise ValueError("summary_prefix and summary_postfix should be provided both ")

        if 'summary_prefix' not in self.__summary or self.__summary['summary_prefix'] != summary_prefix:
            self.__summary['summary_prefix'] = summary_prefix
            self.__summary['summary_postfix'] = summary_postfix

        return self

    def filter(self, *args):
        """
        if argument is a string, it means a condition
        and it always use AND to join conditions, if you want to use complex condition, you could use FQ
        this method should be optimized to support call more than one time
        :param args:
        :param kwargs:
        :return:
        """
        query_temp_list = []
        for item in args:
            if type(item) == list:
                query_temp_list.extend(item)
            else:
                query_temp_list.append(item)

        query_temp_list2 = []
        for item in query_temp_list:
            if type(item) is FQ:
                query_temp_list2.append(item.query_string)
            else:
                query_temp_list2.append(item)
        self.__filter = " AND ".join(query_temp_list2)
        return self

    def config(self, start=0, hit=10, result_format='json', rerank_size='200'):
        """
        config sub search, could multi call this function
        :param start:
        :param hit:
        :param result_format:
        :param rerank_size:
        :return:
        """
        if 'start' not in self.__config or self.__config['start'] != start:
            self.__config['start'] = start
        if 'hit' not in self.__config or self.__config['hit'] != hit:
            self.__config['hit'] = hit
        if 'result_format' not in self.__config or self.__config['result_format'] != result_format:
            self.__config['result_format'] = result_format
        if 'rerank_size' not in self.__config or self.__config['rerank_size'] != rerank_size:
            self.__config['rerank_size'] = rerank_size
        return self

    def query(self, *args, **kwargs):
        """
        if argument is a string, it means default:'argument'
        if argument is a k=v pair, it means k:'v'
        and it always use AND to join conditions, if you want to use complex condition, you could use Q
        :param args:
        :param kwargs:
        :return:
        """

        if self.__query is None:
            self.__query = list()

        query_temp_list = []
        for item in args:
            if type(item) == list:
                query_temp_list.extend(item)
            else:
                query_temp_list.append(item)

        kwargs_query = ["%s:'%s'" % (item[0], item[1]) for item in kwargs.items()]
        query_temp_list.extend(kwargs_query)

        for item in query_temp_list:
            if type(item) is Q:
                self.__query.append(item.query_string)
            else:
                if ":" not in item:
                    log.warning("there is no query index %s, it will be set to default" % item)
                    self.__query.append("default:'%s'" % item)
                else:
                    self.__query.append(item)

        return self

    def rank(self, *args, **kwargs):
        """
        this method will help query to RANK, but you must assign a query first
        :param args:
        :param kwargs:
        :return:
        """
        if len(args) > 0:
            tmp = args[0]
            if ":" not in tmp:
                log.warning("there is no index, it will be set default index")
                query_string = "default:'%s'" % tmp
            else:
                query_string = tmp
        elif len(kwargs) > 0:
            boost = kwargs.get('boost')
            if boost is not None:
                kwargs.pop('boost')

            if len(kwargs) == 0:
                raise ValueError("cannot only assign a boost parameter")

            query_string = "%s:'%s'" % (kwargs.items()[0][0], kwargs.items()[0][1])
        self.__rank = query_string

        return self

    def sort(self, *args):
        """
        could using plaintext to sort, default is +
        class Q also support -Q('field1') and +Q('field2')
        :param args:
        :return:
        """

        if len(args) == 0:
            return self

        sort_items = []

        for item in args:
            item = str(item)
            if not item.startswith("+") and not item.startswith("-"):
                # default is +
                sort_items.append("+%s" % item)
            else:
                sort_items.append(item)
        self.__sort = ";".join(sort_items)
        return self

    def aggregate(self, group_key, agg_fun, range_p=None, agg_filter=None, agg_sampler_threshold=None,
                  agg_sampler_step=None, max_group=None):
        """
        pass aggregate parameters
        :param group_key:
        :param agg_fun:
        :param range_p:
        :param agg_filter:
        :param agg_sampler_threshold:
        :param agg_sampler_step:
        :param max_group:
        :return:
        """

        if self.__aggregate is None:
            self.__aggregate = []

        aggregate_item = {}

        if group_key:
            aggregate_item['group_key'] = group_key
        else:
            raise ValueError("please set a group_key when using aggregate")
        if agg_fun:
            aggregate_item['agg_fun'] = agg_fun
        else:
            raise ValueError("please set a agg_fun when using aggregate")
        if range_p:
            aggregate_item['range'] = range_p
        if agg_filter:
            aggregate_item['agg_filter'] = agg_filter
        if agg_sampler_threshold:
            aggregate_item['agg_sampler_threshold'] = agg_sampler_threshold
        if agg_sampler_step:
            aggregate_item['agg_sampler_step'] = agg_sampler_step
        if max_group:
            aggregate_item['max_group'] = max_group

        self.__aggregate.append(aggregate_item)

        return self

    def distinct(self, dist_key, dist_times=None, dist_count=None,
                 reserved=None, update_total_hit=None, dist_filter=None, grade=None):

        if not dist_key:
            raise ValueError("disk_key required")
        if dist_key:
            if 'dist_key' not in self.__distinct or self.__distinct['dist_key'] != dist_key:
                self.__distinct['dist_key'] = dist_key
        if dist_times:
            if 'dist_times' not in self.__distinct or self.__distinct['dist_times'] != dist_times:
                self.__distinct['dist_times'] = dist_times
        if dist_count:
            if 'dist_count' not in self.__distinct or self.__distinct['dist_count'] != dist_count:
                self.__distinct['dist_count'] = dist_count
        if reserved:
            if 'reserved' not in self.__distinct or self.__distinct['reserved'] != reserved:
                self.__distinct['reserved'] = reserved
        if update_total_hit:
            if 'update_total_hit' not in self.__distinct or self.__distinct['update_total_hit'] != update_total_hit:
                self.__distinct['update_total_hit'] = update_total_hit
        if dist_filter:
            if 'dist_filter' not in self.__distinct or self.__distinct['dist_filter'] != dist_filter:
                self.__distinct['dist_filter'] = dist_filter
        if grade:
            if 'grade' not in self.__distinct or self.__distinct['grade'] != grade:
                self.__distinct['grade'] = grade
        return self

    def kvpairs(self, **kwargs):
        if len(kwargs) > 0:
            self.__kvpairs = ",".join(["%s:%s" % (item[0], item[1]) for item in kwargs.items()])
        return self

    def query_raw(self, query_string):
        """
        pass raw query string, such as:
            query=default:'连衣裙'&&filter=(hit+sale)*rate>10000 AND create_time<1402345600

        ATTENTION:
            if you want to use this method, must call other function first, for example, index_name, kvpairs, etc
        :param param:
        :return:
        """
        self.query_string = query_string
        return self.__result_set()

    def results(self):
        """
        build query strings according to pre settings
        :return:
        """
        self.query_string = self.__build_query_string()
        return self.__result_set()

    def __build_query_string(self):

        # process query and rank
        if self.__query is None:
            raise ValueError("please define a query search")

        query_sub = " AND ".join(self.__query)
        query_sub = query_sub.replace("AND ANDNOT", "ANDNOT")

        if self.__rank is not None:
            query_sub = "(%s) RANK %s" % (query_sub, self.__rank)

        self.sub_searches.append("query=%s" % query_sub)

        # process config
        if self.__config:
            # has set config sub search
            self.sub_searches.append("config=%s" %
                                     ";".join(["%s:%s" % (item[0], item[1]) for item in self.__config.items()]))

        # process filter
        if self.__filter:
            self.sub_searches.append("filter=%s" % self.__filter)

        # process sort
        if self.__sort:
            # has set sort sub search
            self.sub_searches.append("sort=%s" % self.__sort)

        # process aggregate
        if self.__aggregate:
            # has set sort aggregate sub search
            tmp_list = []
            for item in self.__aggregate:
                tmp_list.append(",".join(["%s:%s" % (it[0], it[1]) for it in item.items()]))
            self.sub_searches.append("aggregate=%s" % ";".join(tmp_list))

        # process distinct
        if self.__distinct:
            # has set distinct sub search
            self.sub_searches.append("distinct=%s" %
                                     ",".join(["%s:%s" % (item[0], item[1]) for item in self.__distinct.items()]))

        # process kvpair
        if self.__kvpairs:
            # has set kv pair sub search
            self.sub_searches.append("kvpairs=%s" % self.__kvpairs)

        return "&&".join(self.sub_searches)

    def __result_set(self):
        log.debug("querying %s" % self.query_string)
        self._check_client()
        params = dict()
        if not self.__index_name:
            raise ValueError("must provide an index_name at least")
        params['index_name'] = self.__index_name
        params['query'] = self.query_string

        if self.__fetch_fields:
            params['fetch_fields'] = self.__fetch_fields

        if self.__qp:
            params['qp'] = self.__qp

        if self.__disable:
            params['disable'] = self.__disable

        if self.__first_formula_name:
            params['first_formula_name'] = self.__first_formula_name

        if self.__formula_name:
            params['formula_name'] = self.__formula_name

        if self.__summary:
            params['summary'] = self.__summary

        url = "%s" % Search.BASE_URL

        resp = self.__client.send_message(url, method='GET', params=params)
        resp_info = self.wrap_result(resp)

        return resp_info



