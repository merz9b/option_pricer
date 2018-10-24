#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/10/24 22:52
# @Author  : John
# @File    : setup.py


__author__ = 'Xin Zhang'

from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    require_lists = f.read().split('\n')


setup(
    name='option_tools',
    version=0.1,
    author=__author__,
    author_email='zhangxin_chn@126.com',
    description='Guosen option tools library.',
    keywords='option tools',
    packages=find_packages(),
    include_package_data=True,
    dependency_links=[],
    install_requires=require_lists
)
