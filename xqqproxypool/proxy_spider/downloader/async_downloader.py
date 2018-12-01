# -*- coding: utf-8 -*-
"""
请编写模块注释
"""
__author__ = 'shu2015626'

import json
import asyncio
import aiohttp

from xqqproxypool.utils.log_oper import proj_logger


class AsyncHtmlDownloader(object):
    """
    一个异步下载器，可以对代理源异步抓取，但是容易被BAN。
    """
    def __init__(self):
        self.logger = proj_logger
        self.loop = asyncio.get_event_loop()

    async def _download(self, url, nums_retries=5):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as resp:
                    return await resp.read()
            except Exception:
                if nums_retries > 0:
                    self.logger.warn("Downloading Failure[还有%s次机会尝试]: %s" % (url, nums_retries - 1))
                    await self._download(url, nums_retries - 1)
            return None

    def _run_corotine_function(self, loop, corotine_function, *args, **kwargs):
        # loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(corotine_function(*args, **kwargs))
        # future.add_done_function(func)
        res = loop.run_until_complete(future)
        # loop.close()
        return res

    def download(self, url):
        html = self._run_corotine_function(self.loop, self._download, url)
        if isinstance(html, bytes):
            return html.decode()
        else:
            return html

    def close_resource(self):
        try:
            self.loop.close()
        except:
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_resource()


if __name__ == "__main__":
    url1 = "http://httpbin.org/ip"
    url2 = "http://httpbin.org/headers"
    url3 = "http://httpbin.org/cookies"
    urls = ['http://edmundmartin.com',
               'https://www.udemy.com',
               'https://github.com/',
               'https://zhangslob.github.io/',
               'https://www.zhihu.com/']
    obj = AsyncHtmlDownloader()
    # for url in [url1, url2, url3]:
    for url in urls:
        res = obj.get_html(url)
        print("====================================================================")
        print(res)

    obj.close_resource()


