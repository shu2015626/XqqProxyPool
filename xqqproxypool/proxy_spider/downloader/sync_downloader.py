# -*- coding: utf-8 -*-
"""
实现一个html的下载器
"""
__author__ = 'shu2015626'

import random

import requests
from requests.exceptions import ConnectionError

from xqqproxypool.utils.log_oper import proj_logger
from xqqproxypool.utils.random_user_agent import get_random_ua


class SyncHtmlDownloader(object):
    def __init__(self):
        self.logger = proj_logger

    def _download(self, url, nums_retries=5, options={}):
        try:
            ua = get_random_ua()
        except Exception:
            ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"

        base_headers = {
            'User-Agent':  ua,
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8'
        }
        headers = dict(base_headers, **options)
        self.logger.info('Downloading: ', url)

        proxies = {}
        try:
            proxy_http = requests.get("http://127.0.0.1:5000/get/https", headers=headers).text()
            proxy_https = requests.get("http://127.0.0.1:5000/get/http", headers=headers).text()
            if proxy_http and proxy_http != 'None':
                proxies['http'] = proxy_http
            if proxy_https and proxy_https != 'None':
                proxies['https'] = proxy_https
        except Exception as e:
            print("获取代理准备抓代理网站失败，错误为：\n", e)

        try:
            if proxies:
                resp = requests.get(url, headers=headers, proxies=proxies)
            else:
                resp = requests.get(url, headers=headers)
            self.logger.info('Downloading status: %s(%s)' %(resp.status_code, url))
            if resp.status_code == 200:
                return resp
        except ConnectionError:
            if nums_retries > 0:
                self.logger.warn("Downloading Failure[还有%s次机会尝试]: %s" % (url, nums_retries-1))
                self._download(url, nums_retries-1)
        return None

    def download(self, url):
        resp = self._download(url)
        if resp and resp.status_code == 200:
            return resp.text
        else:
            return None


if __name__ == "__main__":
    url1 = "http://httpbin.org/ip"
    url2 = "http://httpbin.org/headers"
    url3 = "http://httpbin.org/cookies"

    obj = HtmlDownloader()
    for url in [url1, url2, url3]:
        res = obj.get_html(url)
        print("====================================================================")
        print(res)
