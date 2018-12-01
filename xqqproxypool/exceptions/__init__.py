# -*- coding: utf-8 -*-
"""
简化模块导入
"""
__author__ = 'shu2015626'

from .exceptions import ResourceDepletionError, PoolEmptyError

__all__ = ["ResourceDepletionError", "PoolEmptyError"]