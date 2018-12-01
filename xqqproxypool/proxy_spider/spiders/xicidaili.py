# -*- coding: utf-8 -*-
"""
coolproxy
需要加载js
"""
__author__ = 'shu2015626'
import datetime
from bs4 import BeautifulSoup
from .base_spider import ProxyBaseSpider


class XiCiDaiLiSpider(ProxyBaseSpider):
    name = 'xicidaili'
    page_count = 3
    # url = https://www.kuaidaili.com/free/inha/2/
    start_urls = ["http://www.xicidaili.com/nn/{page_no}".format(page_no=i + 1) for i in range(page_count)]

    def parse(self, html):
        if not html:
            return
        proxies_dct = {}
        soup = BeautifulSoup(html, 'lxml')
        active_page = soup.find('em', attrs={"class": "current"}).get_text()
        trs = soup.find('table', attrs={"id": "ip_list"}).find_all("tr", attrs={"class": "odd"})

        if len(trs) < 1:
            return

        proxies_info = []
        ip_seen = set()
        for tr in trs:
            tds = tr.find_all('td')
            anonymity = tds[4].get_text()
            if "高匿" not in anonymity:
                continue

            ip = tds[1].get_text()
            if ip in ip_seen:
                continue
            else:
                ip_seen.add(ip)
            port = tds[2].get_text()
            scheme = tds[5].get_text()
            last_validate_time = tds[9].get_text()
            proxies_info.append((ip, port, scheme, last_validate_time))

        if not proxies_info:
            return

        if active_page and active_page == "1":
            last_validate_time = proxies_info[0][-1]
            last_validate_time = datetime.datetime.strptime(last_validate_time, '%y-%m-%d %H:%M')
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