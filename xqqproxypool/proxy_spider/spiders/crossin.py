# -*- coding: utf-8 -*-
"""
crossin

http://lab.crossincode.com/proxy/
"""
__author__ = 'shu2015626'

import json
from bs4 import BeautifulSoup
from .base_spider import ProxyBaseSpider


class CrossinSpider(ProxyBaseSpider):
    name = 'crossin'
    # page_count = 7
    # url = http://lab.crossincode.com/proxy/
    start_urls = ["http://lab.crossincode.com/proxy/get/?num=15&head=https",
                  "http://lab.crossincode.com/proxy/get/?num=15"]

    def parse(self, html):
        if not html:
            return

        http_lst = []
        https_lst = []
        ip_dct = json.loads(html)
        proxies = ip_dct.get("proxies")
        if proxies:
            for proxy in proxies:
                ip_type = proxy.get("类型")
                if not ip_type or ip_type != "高匿":
                    continue
                last_validate_time = proxy.get("最后验证时间")
                ip_port = proxy.get("http") or proxy.get("https")
                if ip_port:
                    http_lst.append(ip_port)
                    https_lst.append(ip_port)

        proxies_dct = {}
        proxies_dct['http'] = http_lst
        proxies_dct['https'] = https_lst

        return proxies_dct