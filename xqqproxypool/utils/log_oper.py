# -*- coding: utf-8 -*-
"""
封装日志操作
"""
__author__ = 'shu2015626'

import logging

# import os
# try:
#     if os.name == 'posix':
#         import fcntl
#     elif os.name == 'nt':
#         import utils.win_fcntl as fcntl
#     else:
#         raise Exception("不认识的操作系统平台，无法导入fcntl")
# except Exception:
#     raise


proj_logger = logging.getLogger(__name__)