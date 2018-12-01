# -*- coding: utf-8 -*-
"""
自定义一些错误
"""
__author__ = 'shu2015626'


class ResourceDepletionError(Exception):
    def __init__(self, *args, **kwargs):
        super(ResourceDepletionError, self).__init__(*args, **kwargs)

    def __str__(self):
        return repr('The proxy source is exhausted!')


class PoolEmptyError(Exception):
    def __init__(self, *args, **kwargs):
        super(PoolEmptyError, self).__init__(*args, **kwargs)

    def __str__(self):
        return repr('The proxy pool is empty!')

