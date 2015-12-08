# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'barycenter'

from opensearchsdk import utils
from opensearchsdk.core.client import OpensearchClientFactory
from opensearchsdk.service.application import ApplicationMgr
from opensearchsdk.service.data import DataMgr
from opensearchsdk.service.search import Search, Q
from opensearchsdk.config import Config

# if you want to open debug log, please set it to True
Config.DEBUG = True

# create a client, this is singleton
client = OpensearchClientFactory.create_client("hangzhou", "external", "XVqTa2Rl5fGpml7c", "ZRXQN8Azm15Z7bWKgD0zVzS0OJR6A9")

# create a application
# ApplicationMgr is thread safe
app = ApplicationMgr(client)
app_name = utils.get_random_str(6)
# make sure you have created a template named default2 manually
resp = app.create(app_name, "default2")

# you could get mission result by:
if resp.success():
    print("create app %s success" % app_name)

# and you could get return json object
print(resp.result)

# upload to this application a document
# DataMgr is also thread safe
# you could reuse client
data_mgr = DataMgr(client)
json_str = """
        [
            {
                "cmd": "add",
                "timestamp": 1401342874777,
                "fields": {
                    "id": "1",
                    "title": "This is the title",
                    "body": "This is the body"
                }
            },
            {
                "cmd": "update",
                "timestamp": 1401342874778,
                "fields": {
                    "id": "2",
                    "title": "This is the new title"
                }
            },
            {
                "cmd": "delete",
                "fields": {
                    "id": "3"
                }
            }
        ]
        """
resp = data_mgr.upload(app_name, "main", json_str)

# a little like create app's result:
if resp.success():
    print("upload date to %s success" % app_name)

print(resp.result)

# search is NOT thread safe, please create a instance for each query
search = Search(client)
search.query("title").index_name(app_name)
results = search.results()

# search result is also like common result, you could do anything you want when get json object
if results.success():
    print("query success")

print results.result

# if you want to use some complex query, you could use Q, for example
search = Search(client)  # remember, search is NOT thread safe, please create a new one
search.query(Q(default="title"), Q(default="中文") | Q(default="title3")).rank("校长").index_name("F7xBML")
results = search.results()
# Q(xxx) | Q(yyy) means xxx OR yyy, it support & -> AND, | -> OR, ~ -> ANDNOT

# delete this application
app.delete(app_name)

# hope you like it, for more detail usage, you could find in unit test cases
