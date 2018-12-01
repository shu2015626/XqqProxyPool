# -*- coding: utf-8 -*-
"""
请编写模块注释
"""
__author__ = 'shu2015626'

import argparse
# from xqqproxypool.webapi import app
from xqqproxypool.aioapi import main
from xqqproxypool.scheduler import Scheduler


def run():

    # 启动调度器，调度：1.验证代理有效性；2.调用爬虫获取代理
    obj_scheduler = Scheduler()
    obj_scheduler.run()
    # 启动webapi服务，可以通过webapi调用proxy了
    # app.run(host='0.0.0.0', port=1115)
    main()


if __name__ == "__main__":
    run()