# -*- coding: utf-8 -*-
"""
爬取西祠代理
"""
__author__ = 'shu2015626'
import datetime
from bs4 import BeautifulSoup
from .base_spider import ProxyBaseSpider


class Data5uSpider(ProxyBaseSpider):
    name = 'data5u'
    # page_count = 3
    # url = http://www.data5u.com/free/gngn/index.shtml
    daili_types = ['gngn']
    start_urls = ["http://www.data5u.com/free/{daili_type}/index.shtml".format(daili_type=daili_type) for daili_type in daili_types]

    def parse(self, html):
        if not html:
            return
        proxies_dct = {}
        soup = BeautifulSoup(html, 'lxml')
        # active_page = soup.find('em', attrs={"class": "current"}).get_text()
        lis = soup.find_all('div', attrs={"class": "wlist"})[1].find_all("ul", attrs={"class": "l2"})
        if len(lis) < 1:
            return

        proxies_info = []
        ip_seen = set()
        for li in lis:
            spans = li.find_all('span')
            anonymity = spans[2].get_text()
            if "高匿" not in anonymity:
                continue
            ip = spans[0].get_text()
            if ip in ip_seen:
                continue
            else:
                ip_seen.add(ip)
            port = spans[1].get_text()
            scheme = spans[3].get_text()
            last_validate_time = spans[8].get_text()
            proxies_info.append((ip, port, scheme, last_validate_time))

        if not proxies_info:
            return

        http_lst = []
        https_lst = []
        for ip, port, scheme, _ in proxies_info:
            # 若不管代理的scheme是啥，所有对列都要加入。只需随便更改一下scheme即可
            scheme = ""
            if scheme.lower() == "http":
                proxy = ip + ":" + port
                http_lst.append(proxy)
            elif scheme.lower() == "https":
                proxy = ip + ":" + port
                https_lst.append(proxy)
            else:
                proxy = ip + ":" + port
                https_lst.append(proxy)
                http_lst.append(proxy)

        proxies_dct['http'] = http_lst
        proxies_dct['https'] = https_lst

        return proxies_dct