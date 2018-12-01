# -*- coding: utf-8 -*-
"""
爬取西祠代理
"""
__author__ = 'shu2015626'

from .base_spider import ProxyBaseSpider


class A2uSpider(ProxyBaseSpider):
    name = 'a2u'
    # page_count = 3
    # url = https://raw.githubusercontent.com/a2u/free-proxy-list/master/free-proxy-list.txt
    # 这是一个txt的文本
    start_urls = ["https://raw.githubusercontent.com/a2u/free-proxy-list/master/free-proxy-list.txt"]

    def parse(self, html):
        if not html:
            return
        proxies_dct = {}
        proxies = [proxy.strip() for proxy in html.strip().split("\n") if proxy.strip()]
        proxies_dct['http'] = proxies
        proxies_dct['https'] = proxies

        return proxies_dct