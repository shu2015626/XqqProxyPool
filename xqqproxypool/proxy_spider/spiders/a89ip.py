# -*- coding: utf-8 -*-
"""
爬取89ip
"""
__author__ = 'shu2015626'
import datetime
from bs4 import BeautifulSoup
from .base_spider import ProxyBaseSpider


class A89IPSpider(ProxyBaseSpider):
    name = '89ip'
    page_count = 9
    # url = http://www.89ip.cn/index_1.html
    start_urls = ["http://www.89ip.cn/index_{page_no}.html".format(page_no=i+1) for i in range(page_count)]

    def parse(self, html):
        if not html:
            return
        proxies_dct = {}
        soup = BeautifulSoup(html, 'lxml')
        # active_page = soup.find('em', attrs={"class": "current"}).get_text()
        trs = soup.find('table', attrs={"class": "layui-table"}).find('tbody').find_all("tr")
        if len(trs) < 1:
            return

        proxies_info = []
        ip_seen = set()
        for tr in trs:
            tds = tr.find_all('td')
            ip = tds[0].get_text().strip()
            if ip in ip_seen:
                continue
            else:
                ip_seen.add(ip)
            port = tds[1].get_text().strip()
            scheme = ""
            # last_validate_time = tds[4].get_text().strip()
            last_validate_time = ""
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