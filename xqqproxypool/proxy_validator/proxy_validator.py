# -*- coding: utf-8 -*-
"""
请编写模块注释
"""
__author__ = 'shu2015626'
import asyncio
import aiohttp
import requests
import json
import functools

from ..config.settings import VALIDATE_URL, PROXY_RETURN_TIMEOUT
from xqqproxypool.utils.random_user_agent import get_random_ua
from xqqproxypool.dboper.redis_oper import RedisOper


class ProxiesValidator(object):
    validate_url = VALIDATE_URL

    def __init__(self):
        self._raw_proxies = None
        self._usable_proxies = []

    def set_raw_proxies(self, proxies):
        self._raw_proxies = proxies
        self._obj_redis = RedisOper()

    async def _validate_one_proxy(self, scheme, proxy):
        """
        测试一个proxy, 如果可用加入到self._usable_proxies队列
        否则直接pass掉
        :param proxy:
        :return:
        """
        try:
            async with aiohttp.ClientSession() as session:
                try:
                    if isinstance(proxy, bytes):
                        proxy = proxy.decode('utf-8')

                    # real_proxy = scheme + "://" + proxy
                    real_proxy = "http://" + proxy  # aiohttp只支持http代理
                    real_validate_url = scheme + "://" + self.validate_url
                    print("-- Validating proxy: ", real_proxy)
                    headers = {"User-Agent": get_random_ua()}
                    # ====================================================================
                    async with session.get(real_validate_url, proxy=real_proxy, headers=headers, timeout=PROXY_RETURN_TIMEOUT) as response:
                        # 简单的这样可能是因为暴露了本机ip,因此还是采用httpbin.org比较好
                        return await response.text()
                        # if response.status == 200:
                        #     self._obj_redis.rpush_proxy(scheme, proxy)
                        #     print("** Valid proxy: ", real_proxy)
                    # ====================================================================
                    # 太慢了
                    # proxies = {"http": proxy, "https": proxy}
                    # with requests.get(real_validate_url, proxies=proxies, headers=headers, timeout=PROXY_RETURN_TIMEOUT) as response:
                    #     if response and response.status_code == 200:
                    #         # # 使用httpbin/ip验证时
                    #         # ip_dct = response.json()
                    #         # if not (ip_dct["origin"] == proxy.split(":")[0]):
                    #         #     return
                    #         self._obj_redis.rpush_proxy(scheme, proxy)
                    #         print("** Valid proxy: ", proxy)
                    # ====================================================================
                except Exception:
                    print('xx Invalid proxy: ', proxy)
        except Exception as e:
            print(e)

    # def validate(self, scheme):
    #     """
    #     适用于只采用200状态码判断的情况
    #     :param scheme:
    #     :return:
    #     """
    #     print("Validator is working……")
    #     loop = asyncio.get_event_loop()
    #     try:
    #         tasks = [self._validate_one_proxy(scheme, proxy) for proxy in self._raw_proxies]
    #         loop.run_until_complete(asyncio.gather(*tasks))
    #     except Exception as e:
    #         print('Async Validate Proxy Error! 错位为: \n %s' % e)

    def _validate_one_proxy_callback(self, scheme, proxy, future):
        try:
            text = future.result()
            if not text:
                return
            ip = json.loads(text)['origin']
            if proxy.split(":")[0] == ip:
                self._obj_redis.rpush_proxy(scheme, proxy)
                print("** Valid proxy: ", proxy)
        except Exception:
            print("xx Invalid proxy: ", proxy)

    def validate(self, scheme):
        """
        采用httpbin/ip的返回值判断

        :param scheme:
        :return:
        """
        print("Validator is working……")
        loop = asyncio.get_event_loop()
        try:
            tasks = []
            for proxy in self._raw_proxies:
                future = asyncio.ensure_future(self._validate_one_proxy(scheme, proxy))
                future.add_done_callback(functools.partial(self._validate_one_proxy_callback, *(scheme, proxy)))
                tasks.append(future)
            loop.run_until_complete(asyncio.gather(*tasks))
        except Exception as e:
            print('Async Validate Proxy Error! 错位为: \n %s' % e)

