# aliyun-opensearch-python-sdk

Welcome to aliyun-opensearch-python-sdk, this sdk provides you with simple and efficient method to use aliyun 
opensearch service.

created by cicero, zhaorbox@gmail.com

## Installation

Install this sdk from source code:

```
python setup.py install
```

## Usage
Please refer to sample.py for general information

Here list some information about query

### query
you have three methods to trigger a query

search class could be write as link expression, each clause is a method

client = OpensearchClientFactory.create_client("hangzhou", "external", "accessKeyId", "accessKey")
search = Search(self.client)

1. simple way, you could search.query("default:'阿里巴巴'", "default:'阿里妈妈'").index_name(app_name)
   it means query=default:'阿里巴巴' AND default:'阿里妈妈'
   
2. combination complex query condition using Q
   search.query(Q(default="title"), Q(default="中文")|Q(default="title3")).rank("校长").index_name(app_name1, app_name2)
   Please notice index_name is essential, and it supports multi application name :)
   
    Q is support all operates:
    
        Q(1) | Q(2) => default:'1' OR default:'2'
        Q(1) & Q(2) => default:'1' AND default:'2'
        Q(a=1), Q(2) | Q(3) => a:'1' AND (default:'2' OR default:'3')
        Q(a=1) & Q(b=2) | Q(c=3) => a:'1' AND b:'2' OR c:'3'
        Q(a=1), ~Q(b=2) => a:'1' ANDNOT b:'2'
   
   if you want to add RANK, rank() method will help you, please refer to test_search.py

3. too complicated query string... you think class Q can not be used, query_raw() method will help you execute plain query string

### config
use config() method, the parameter is refer to http://help.aliyun.com/document_detail/opensearch/api-reference/query-clause/config-clause.html

### filter
use filter() method, the filter conditional is a little like query clause, just use FQ to combine complex filter rule

### sort
use sort() method

### aggregate
use aggregate() method, if you have more than one group parameter, you could call this method multi times, each time add a group parameter. for more parameter information, please refer to http://help.aliyun.com/document_detail/opensearch/api-reference/query-clause/aggregate-clause.html 

### distinct
use distinct() method, please refer to http://help.aliyun.com/document_detail/opensearch/api-reference/query-clause/distinct-clause.html for parameter's usage

### kvpairs
use kvpairs() method

## Development


## Contributing

Bug reports and pull requests are welcome on GitHub at http://git.oschina.net/cicero-zhao/aliyun-opensearch-python-sdk. 
This project is intended to be a safe, welcoming space for collaboration, and contributors are expected to adhere to 
the [Contributor Covenant](contributor-covenant.org) code of conduct.

## License

This library is distributed under the
[Apache License, version 2.0](http://www.apache.org/licenses/LICENSE-2.0.html)

```no-highlight

copyright information: XXXX

licensed under the apache license, version 2.0 (the "license");
you may not use this file except in compliance with the license.
you may obtain a copy of the license at

    http://www.apache.org/licenses/license-2.0

unless required by applicable law or agreed to in writing, software
distributed under the license is distributed on an "as is" basis,
without warranties or conditions of any kind, either express or implied.
see the license for the specific language governing permissions and
limitations under the license.
```
