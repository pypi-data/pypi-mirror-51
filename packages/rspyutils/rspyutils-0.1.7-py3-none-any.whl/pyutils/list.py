# !/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created on MAY 21, 2018
@author: zhanglanhui
homepage recommender:ffm
"""
import copy


def _list_merge(l1, l2):
    # 将所有的漫画按照type分类
    tmp = copy.deepcopy(l1)
    tmp.extend([x for x in l2 if x not in l1])
    return tmp


def check_length(l, length):
    if len(l) < length:
        raise ValueError("len of list is less then {}".format(length))
