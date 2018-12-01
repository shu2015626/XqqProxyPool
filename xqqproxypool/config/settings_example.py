# -*- coding: utf-8 -*-
"""
配置项目的全局变量
"""
__author__ = 'shu2015626'

# 网站应该支持http和https两种访问方式，如果换成百度,需要去改一下验证器
# VALIDATE_URL = "www.baidu.com"
VALIDATE_URL = "httpbin.org/ip"

# 测试代理, 可以忍受的时间界限
PROXY_RETURN_TIMEOUT = 15

# 代理池数量界限
PROXY_POOLSIZE_LOWER_THRESHOLD = 10
PROXY_POOLSIZE_UPPER_THRESHOLD = 20

# 检查周期。
# 这两个参数应该结合“代理可以忍受的超时时间”确定
PROXY_VALIDATE_CYCLE = 60  # 多久验证一次代理池里的代理是否可用，只有验证有效性才会改变池子的大小
PROXY_POOLSIZE_CHECK_CYCLE = 20  # 多久检查一次代理池中代理的数量，主要用来触发爬虫
# 每次验证池子中多少比例测的代理
PROXY_VALIDATE_RATIO = 0.7

# redis相关
REDIS_MODE = "single"  # 可以是single, sentinel, cluster的一种
if REDIS_MODE == "single":
    REDIS_SETTINGS_DCT = {
        "redis_host": 'localhost',
        "redis_port": 6379,
        "redis_db_num": 0,
        # "redis_passwd": '',
    }
elif REDIS_MODE == "sentinel":
    REDIS_SETTINGS_DCT = {
        "redis_sentinel_servers": [("127.0.0.1", '27000'), ("127.0.0.1", '27001'), ("127.0.0.1", '27002')],
        "redis_master_name": "mymaster",
        "redis_db_num": 0,
        "redis_passwd": '',
    }
elif REDIS_MODE == "cluster":
    REDIS_SETTINGS_DCT = {
        "redis_cluster_nodes": [
                                {"host": "127.0.0.1", "port": "8000"},
                                {"host": "127.0.0.1", "port": "8001"},
                                {"host": "127.0.0.1", "port": "8002"},
                                {"host": "127.0.0.1", "port": "8003"},
                                {"host": "127.0.0.1", "port": "8004"},
                                {"host": "127.0.0.1", "port": "8005"},
                                ],
        "redis_passwd": '',
    }

# 队列名称, 这个没用到
# PROXIES_HTTP = "proxies:http"
# PROXIES_HTTPS = "proxies:https"
