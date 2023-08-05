# -*- coding:utf-8 -*-
"""
@Author : Roy
@Time : 2019/8/19 10:56
@Company : qb
"""


from setuptools import setup

setup(
    name='qb-consul',
    version='1.0.1',
    author='Roy',
    author_email='1573277807@qq.com',
    url='http://www.qibao-tech.com',
    description='consul服务注册与获取',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    packages=['qb_consul'],
    install_requires=['python-consul>=1.1.0'],
)
