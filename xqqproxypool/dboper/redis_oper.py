# -*- coding: utf-8 -*-
"""
封装redis操作
"""
__author__ = 'shu2015626'

from redis import StrictRedis
from redis.sentinel import Sentinel
from rediscluster import StrictRedisCluster

from ..config.settings import REDIS_SETTINGS_DCT, REDIS_MODE
from ..exceptions import PoolEmptyError
from ..utils.log_oper import proj_logger


class RedisOper(object):
    def __init__(self, redis_mode=REDIS_MODE):
        self.redis_mode = redis_mode
        if redis_mode == "single":
            passwd = REDIS_SETTINGS_DCT.get("redis_passwd", None)
            if passwd:
                self.__redis_client = StrictRedis(host=REDIS_SETTINGS_DCT.get("redis_host"), port=REDIS_SETTINGS_DCT.get("redis_port"),
                                                db=REDIS_SETTINGS_DCT.get("redis_db_num"), password=passwd,
                                                socket_timeout=5, socket_connect_timeout=5, decode_responses=True)
            else:
                self.__redis_client = StrictRedis(host=REDIS_SETTINGS_DCT.get("redis_host"), port=REDIS_SETTINGS_DCT.get("redis_port"),
                                                db=REDIS_SETTINGS_DCT.get("redis_db_num"), socket_timeout=5,
                                                socket_connect_timeout=5, decode_responses=True)
        elif redis_mode == "sentinel":
            passwd = REDIS_SETTINGS_DCT.get("redis_passwd", None)
            if passwd:
                obj_sentinel = Sentinel(sentinels=REDIS_SETTINGS_DCT.get('redis_sentinel_servers'), password=passwd,
                                        db=REDIS_SETTINGS_DCT.get("redis_db_num"), socket_timeout=5,
                                        socket_connect_timeout=5, decode_responses=True)
                self.__redis_client = obj_sentinel.master_for(service_name=REDIS_SETTINGS_DCT.get('redis_master_name'))
            else:
                obj_sentinel = Sentinel(sentinels=REDIS_SETTINGS_DCT.get('redis_sentinel_servers'),
                                        db=REDIS_SETTINGS_DCT.get("redis_db_num"), socket_timeout=5,
                                        socket_connect_timeout=5, decode_responses=True)
                self.__redis_client = obj_sentinel.master_for(service_name=REDIS_SETTINGS_DCT.get('redis_master_name'))
        elif redis_mode == "cluster":
            passwd = REDIS_SETTINGS_DCT.get("redis_passwd", None)
            if passwd:
                self.__redis_client = StrictRedisCluster(startup_nodes=REDIS_SETTINGS_DCT.get("redis_cluster_nodes"),
                                                       password=passwd, decode_responses=True)
            else:
                self.__redis_client = StrictRedisCluster(startup_nodes=REDIS_SETTINGS_DCT.get("redis_cluster_nodes"),
                                                       decode_responses=True)
        else:
            proj_logger.error("不支持的redis模式: %s" % str(redis_mode))
            self.__redis_client = None

    def lget_proxies(self, scheme, count=1):
        """
        从redis队列（左端）中取出count个代理，是批量操作
        主要是正在验证代理有效性时使用。

        :param scheme: 要取出的代理类型,应该是http/https
        :param count: 取出的代理数量
        :return:
        """
        key = "proxies:" + str(scheme)
        proxies = self.__redis_client.lrange(key, 0, count-1)
        self.__redis_client.ltrim(key, count, -1)
        return proxies

    def lpush_proxy(self, scheme, proxy):
        """
        从队列左端插入一个代理。
        主要是，将新爬取的代理从左端插入
        :param scheme:
        :param proxy:
        :return:
        """
        key = "proxies:" + str(scheme)
        self.__redis_client.lpush(key, proxy)

    def rpush_proxy(self, scheme, proxy):
        """
        从队列右端插入一个代理。
        主要是，将验证有效的代理从右端插回
        :param scheme:
        :param proxy:
        :return:
        """
        key = "proxies:" + str(scheme)
        self.__redis_client.rpush(key, proxy)

    def rpop_proxy(self, scheme):
        """
        从队列右端弹出一个代理，以供使用，但同时从左端插回队列
        我的想法是，不能使用一次就从队列删除。使用的时候不删除
        所有的删除操作都应该交给验证程序，只有验证程序认为无效才删除

        :param scheme: http或者https，表示从哪个队列中取出代理
        :return:
        """
        key = "proxies:" + scheme
        try:
            return self.__redis_client.rpoplpush(key, key)
        except:
            raise PoolEmptyError

    def get_proxies_nums(self, scheme):
        """
        获取队列长度，即获得可用队列长度

        :param scheme: http或者https,表示获取哪个队列
        :return:
        """
        key = "proxies:" + scheme
        return self.__redis_client.llen(key)

    def flushdb(self):
        """
        清空数据。
        不能使用flushall, 因为在sentinel或者单机（包括主备模式），会清空16个db的数据
        :return:
        """
        self.__redis_client.flushdb()


if __name__ == "__main__":
    obj_redis_oper = RedisOper("single")
    obj_redis_oper.rpop_proxy("http")