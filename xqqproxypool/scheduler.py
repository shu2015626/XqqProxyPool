# -*- coding: utf-8 -*-
"""
调度器：
1.调度验证器：验证proxy可用
2.调度爬虫：通过检查代理池状态，确认是否要调用爬虫抓取代理。代理在加入代理池前也要
"""
__author__ = 'shu2015626'

import time
import multiprocessing
from multiprocessing import Process

from .proxy_spider.spider_main import SpiderMain
from .proxy_validator import ProxiesValidator
from xqqproxypool.dboper import RedisOper
from xqqproxypool.config.settings import PROXY_VALIDATE_CYCLE, PROXY_VALIDATE_RATIO
from xqqproxypool.config.settings import PROXY_POOLSIZE_CHECK_CYCLE, PROXY_POOLSIZE_LOWER_THRESHOLD, PROXY_POOLSIZE_UPPER_THRESHOLD


class Scheduler(object):
    """
    调度器：
    1.调度验证器：验证proxy可用
    2.调度爬虫：通过检查代理池状态，确认是否要调用爬虫抓取代理
    """
    @staticmethod
    def check_pool(poolsize_lower_threshold=PROXY_POOLSIZE_LOWER_THRESHOLD,
                   poolsize_upper_threshold=PROXY_POOLSIZE_UPPER_THRESHOLD,
                   cycle=PROXY_POOLSIZE_CHECK_CYCLE):
        """
        检查代理池，如果数量不对，
        调用爬虫获取IP
        :return:
        """
        spider = SpiderMain()  # 爬虫
        obj_redis = RedisOper()
        while True:
            poolsize_http = obj_redis.get_proxies_nums('http')
            poolsize_https = obj_redis.get_proxies_nums('https')
            half_poolsize_lower_threshold = int(0.5 * poolsize_lower_threshold)
            if poolsize_http < half_poolsize_lower_threshold or poolsize_https< half_poolsize_lower_threshold:
                print('Proxy pool<http> has %s proxies. Proxy pool<https> has %s proxies.'
                      'while half poolsize of lower_threshold  is %s. '
                      'Starting spider' % (poolsize_http, poolsize_https, half_poolsize_lower_threshold))
                half_poolsize_upper_threshold = int(0.5*poolsize_upper_threshold)
                spider.run(half_poolsize_upper_threshold)
            time.sleep(cycle)

    @staticmethod
    def validate_proxies(cycle=PROXY_VALIDATE_CYCLE):
        """
        验证代理
        :return:
        """
        validator = ProxiesValidator()
        obj_redis = RedisOper()

        while True:
            print('Refreshing ips......')
            for scheme in ['http', 'https']:
                poolsize = obj_redis.get_proxies_nums(scheme)
                count = int(PROXY_VALIDATE_RATIO * poolsize)
                if count == 0:
                    print('Proxy pool<%s> is empty. Waiting for adding....' % scheme)
                    time.sleep(0.5 * cycle)
                raw_proxies = obj_redis.lget_proxies(scheme, count)
                validator.set_raw_proxies(raw_proxies)
                validator.validate(scheme)

    def run(self):
        print("Ip Processing is running......")
        processes = []
        validate_process = Process(target=Scheduler.validate_proxies, name="validate_process")
        check_process = Process(target=Scheduler.check_pool, name="check_process")
        validate_process.start()
        check_process.start()
        # processes.append(validate_process)
        # processes.append(check_process)
        # while True:
        #     for p in processes:
        #         if not p.is_alive():
        #             print("子进程<%s>死掉了！" % p.name)
        #     print("当前活着的进程数为：%s" % len(multiprocessing.active_children()))
        #     time.sleep(10)



