# -*- coding: utf-8 -*-
"""
请编写模块注释
"""
__author__ = 'shu2015626'

from ..downloader import SyncHtmlDownloader
# from ..outputer import Outputer
from xqqproxypool.proxy_validator import ProxiesValidator


class ProxyBaseSpider(object):
    name = "free_proxy"
    start_urls = []

    def __init__(self):
        self.downloader = SyncHtmlDownloader()
        # self.outputer = Outputer()
        self.validator = ProxiesValidator()

    def parse(self, html):
        """
        需要解析页面，获得两个队列, 以字典形式返回
        proxies_dct = {
            "http": [],
            "https": [],
        }
        :param html:
        :return:
        """
        raise NotImplemented

    def make_request(self, url=None):
        if url:
            yield self.downloader.download(url)
        elif self.start_urls:  # and url not in self.start_urls:
            for url in self.start_urls:
                yield self.downloader.download(url)
        else:
            yield None

    def crawl(self, url=None):
        for html in self.make_request(url):
            proxies_dct = self.parse(html)
            if not proxies_dct:
                return
            for scheme, proxy_lst in proxies_dct.items():
                # 新爬取的代理在验证之后加入队列
                self.validator.set_raw_proxies(proxy_lst)
                self.validator.validate(scheme)
                # 不需要输出器，输出到redis的代理池，通过验证器来做
                # self.outputer.output2redis(scheme, proxy_lst)


