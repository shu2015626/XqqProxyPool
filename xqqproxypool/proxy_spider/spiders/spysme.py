# -*- coding: utf-8 -*-
"""
爬取spys.me
"""
__author__ = 'shu2015626'
import re
from .base_spider import ProxyBaseSpider


class SpysMeSpider(ProxyBaseSpider):
    name = 'spysme'
    # page_count = 3
    # url = 'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt'
    # 这是一个txt的文本
    start_urls = ['https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt']

    def parse(self, html):
        if not html:
            return
        proxies_dct = {}
        # last_update_time = re.search(r"updated at (.*)\s+Mirror", html, re.S).group(1)
        proxies_info = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}) \w+-(\w+?).*?', html)
        proxies = [proxy.strip() for proxy, anonymity in proxies_info if proxy.strip() and anonymity != 'N']
        proxies_dct['http'] = proxies
        proxies_dct['https'] = proxies

        return proxies_dct