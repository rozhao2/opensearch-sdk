# -*- encoding: utf-8 -*-
__author__ = 'barycenter'

import setuptools

setuptools.setup(
    name="aliyun-opensearch-sdk",
    version="1.0.0",
    author="zhaorong",
    author_email="zhao_rong@live.com",
    description="aliyun opensearch python sdk",
    license="Apache License Version 2.0",
    url="https://git.oschina.net/cicero-zhao/aliyun-opensearch-python-sdk.git",
    install_requires=[
        "requests",
        "six"
    ],
    packages=['opensearchsdk'],
    classifiers=[
        "Development Satus :: 1 - Pre-alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache License Version 2.0",
        "Operating System :: OS Independent",
        "Programing Language :: python"
    ],
)


