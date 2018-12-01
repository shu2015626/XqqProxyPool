# -*- coding: utf-8 -*-
"""
爬取proxylistplus
"""
__author__ = 'shu2015626'
import datetime
from bs4 import BeautifulSoup
from .base_spider import ProxyBaseSpider


class ProxyListPlusSpider(ProxyBaseSpider):
    name = 'proxylistplus'
    page_count = 3
    # url = https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-2
    start_urls = ["https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-{page_no}".format(page_no=i+1) for i in range(page_count)]

    def parse(self, html):
        if not html:
            return
        proxies_dct = {}
        soup = BeautifulSoup(html, 'lxml')
        # active_page = soup.find('em', attrs={"class": "current"}).get_text()
        trs = soup.find('table', attrs={"class": "bg"}).find_all("tr", attrs={"onmouseover": True})
        if len(trs) < 1:
            return

        proxies_info = []
        ip_seen = set()
        for tr in trs:
            tds = tr.find_all('td')
            anonymity = tds[3].get_text()
            if "anonymous" not in anonymity:
                continue
            ip = tds[1].get_text()
            port = tds[2].get_text()
            if ip in ip_seen:
                continue
            else:
                ip_seen.add(ip)
            is_https = tds[6].get_text()
            if is_https and is_https.strip() == "yes":
                scheme = "https"
            elif is_https and is_https.strip() == "no":
                scheme = "http"
            else:
                scheme = ""
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