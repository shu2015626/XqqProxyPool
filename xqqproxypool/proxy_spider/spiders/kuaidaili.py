# -*- coding: utf-8 -*-
"""
爬取快代理
"""
import datetime

__author__ = 'shu2015626'

from bs4 import BeautifulSoup
import re
from .base_spider import ProxyBaseSpider


class KuaiDaiLiSpider(ProxyBaseSpider):
    name = 'kuaidaili'
    page_count = 4
    # url = https://www.kuaidaili.com/free/inha/2/
    start_urls = ["https://www.kuaidaili.com/free/inha/{page_no}/".format(page_no=i + 1) for i in range(page_count)]

    def parse(self, html):
        if not html:
            return
        proxies_dct = {}
        active_page = re.search(r'<li>.*?<a.*?class="active">(\d+)</a>', html, re.S).group(1)
        pattern = re.compile(r'<td data-title="IP">(.*?)</td>.*?data-title="PORT">(.*?)</td>' +
                             r'.*?data-title="类型">(.*?)</td>.*?data-title="最后验证时间">(.*?)</td>', re.S)
        proxies_info = re.findall(pattern, html)

        if not proxies_info:
            return

        if active_page and active_page == "1":
            last_validate_time = proxies_info[0][-1]
            last_validate_time = datetime.datetime.strptime(last_validate_time, '%Y-%m-%d %H:%M:%S')
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



