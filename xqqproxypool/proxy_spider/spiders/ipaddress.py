# -*- coding: utf-8 -*-
"""
爬取ipaddress
国外网站
"""
__author__ = 'shu2015626'
import datetime
from bs4 import BeautifulSoup
from .base_spider import ProxyBaseSpider


class IpAddressSpider(ProxyBaseSpider):
    name = 'ipaddress'
    # page_count = 3
    # url = https://www.ipaddress.com/proxy-list/
    start_urls = ["https://www.ipaddress.com/proxy-list/"]

    def parse(self, html):
        if not html:
            return
        proxies_dct = {}
        soup = BeautifulSoup(html, 'lxml')
        # active_page = soup.find('em', attrs={"class": "current"}).get_text()
        trs = soup.find('table', attrs={"class": "proxylist"}).find_all("tr")
        if len(trs) <= 1:
            return

        proxies_info = []
        ip_seen = set()
        for tr in trs[1:]:
            tds = tr.find_all('td')
            anonymity = tds[1].get_text()
            if "anonymous" not in anonymity:
                continue
            ip_port = tds[0].get_text()
            ip = ip_port.split(":")[0]
            port = ip_port.split(":")[1]
            if ip in ip_seen:
                continue
            else:
                ip_seen.add(ip)
            scheme = ""
            last_validate_time = tds[3].get_text()
            proxies_info.append((ip, port, scheme, last_validate_time))

        if not proxies_info:
            return

        last_validate_time = proxies_info[0][-1]
        last_validate_time = datetime.datetime.strptime(last_validate_time, '%Y-%m-%d %H:%M')
        days_of_no_validate = (datetime.datetime.now() - last_validate_time).days
        if days_of_no_validate > 7:
            print("%s天没有更新了……" % str(days_of_no_validate))

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