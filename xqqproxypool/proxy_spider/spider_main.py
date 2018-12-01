# -*- coding: utf-8 -*-
"""
爬虫的总调度程序
"""
__author__ = 'shu2015626'

# 国内
from .spiders.kuaidaili import KuaiDaiLiSpider
from .spiders.xicidaili import XiCiDaiLiSpider
from .spiders.data5u import Data5uSpider
from .spiders.guobanjia import GuoBanJiaSpider
from .spiders.a89ip import A89IPSpider
from .spiders.ip3366 import Ip3366Spider
from .spiders.swei360 import Swei360Spider
from .spiders.crossin import CrossinSpider
# 应该也是国外的吧
from .spiders.spysme import SpysMeSpider
from .spiders.a2u import A2uSpider
# 国外
from .spiders.ipaddress import IpAddressSpider
from .spiders.proxylistplus import ProxyListPlusSpider
from xqqproxypool.dboper.redis_oper import RedisOper


class SpiderMain(object):
    def __init__(self):
        self._obj_redis = RedisOper()
        self._set_spiders()

    def _set_spiders(self):
        self._spiders = set()  # 将爬虫实例加入，无序状态
        try:
            obj_kuaidaili = KuaiDaiLiSpider()
            obj_xicidaili = XiCiDaiLiSpider()
            obj_data5u = Data5uSpider()
            obj_guobanjia = GuoBanJiaSpider()
            obj_a2u = A2uSpider()
            obj_ipaddress = IpAddressSpider()
            obj_proxylistplus = ProxyListPlusSpider()
            obj_spysme = SpysMeSpider()
            obj_89ip = A89IPSpider()
            obj_ip3366 = Ip3366Spider()
            obj_swei360 = Swei360Spider()
            # obj_crossin = CrossinSpider()
            self._spiders.add(obj_kuaidaili)
            self._spiders.add(obj_xicidaili)
            self._spiders.add(obj_data5u)
            self._spiders.add(obj_guobanjia)
            self._spiders.add(obj_ipaddress)
            self._spiders.add(obj_proxylistplus)
            self._spiders.add(obj_spysme)
            self._spiders.add(obj_89ip)
            self._spiders.add(obj_ip3366)
            self._spiders.add(obj_swei360)
            # self._spiders.add(obj_crossin)
        except Exception:
            print("实例化爬虫出错")

    def run(self, upper_poolsize_threshold):
        """
        每运行一个爬虫前，都检查下是否达到了爬虫池设定的上线
        如果达到了，就停止运行。
        :param upper_poolsize_threshold:
        :return:
        """
        try:
            for spider in self._spiders:
                try:
                    poolsize_http = self._obj_redis.get_proxies_nums('http')
                    poolsize_https = self._obj_redis.get_proxies_nums('https')
                    if poolsize_http > upper_poolsize_threshold and poolsize_https > upper_poolsize_threshold:
                        break
                    print("正在抓取：%s" % spider.name)
                    spider.crawl()
                except Exception as e:
                    print("<%s>获取代理IP失败, 错位为:\n %s" % (spider.name, e))
        except Exception as e:
            print(e)


if __name__ == "__main__":
    obj_spider = SpiderMain()
    obj_spider.run()
