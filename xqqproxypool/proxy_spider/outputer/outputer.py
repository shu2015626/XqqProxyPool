# -*- coding: utf-8 -*-
"""
请编写模块注释
"""
__author__ = 'shu2015626'

from xqqproxypool.dboper import RedisOper


class Outputer(object):
    def __init__(self):
        self._obj_redis = RedisOper()

    def output2redis(self, scheme, proxy_lst):
        for proxy in proxy_lst:
            if proxy:
                self._obj_redis.lpush_proxy(scheme, proxy)

