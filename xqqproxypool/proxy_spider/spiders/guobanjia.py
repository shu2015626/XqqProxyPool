# -*- coding: utf-8 -*-
"""
爬取西祠代理
"""
__author__ = 'shu2015626'
import datetime
from bs4 import BeautifulSoup
from .base_spider import ProxyBaseSpider


class GuoBanJiaSpider(ProxyBaseSpider):
    name = 'guobanjia'
    # page_count = 3
    # url = http://www.goubanjia.com/
    start_urls = ["http://www.goubanjia.com/"]

    def parse(self, html):
        if not html:
            return
        proxies_dct = {}
        soup = BeautifulSoup(html, 'lxml')
        # active_page = soup.find('em', attrs={"class": "current"}).get_text()
        trs = soup.find('div', attrs={"class": "row-fluid"}).find('tbody').find_all("tr", attrs={"class": "warning"})
        if len(trs) < 1:
            return

        proxies_info = []
        ip_seen = set()
        for tr in trs:
            tds = tr.find_all('td')
            anonymity = tds[1].get_text()
            if "高匿" not in anonymity:
                continue
            ip_td = tds[0]  # 加了很多干扰项，要先去掉
            _ = [p.extract() for p in ip_td(["p"])]
            ip_port = ip_td.get_text()
            ip = ip_port.split(":")[0]
            port = ip_port.split(":")[1]
            if ip in ip_seen:
                continue
            else:
                ip_seen.add(ip)
            scheme = tds[2].get_text()
            last_validate_time = tds[6].get_text()
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