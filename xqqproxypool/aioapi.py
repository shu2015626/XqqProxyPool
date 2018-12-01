# -*- coding:utf-8 -*-
from aiohttp import web
from xqqproxypool.dboper.redis_oper import RedisOper


def get_redis_connection():
    """
    open a new redis connection if there is none
    yet for the current application context.
    :return:
    """
    redis_client = RedisOper()
    return redis_client


async def index(request):
    html = """
    <html>
        <head>
            <title>xqq's free proxies</title>
        </head>
        <body>
            <h1 align="center">Welcome to Xqq Free Proxy Pool System!</h1>  
            <div>
                <p>You can get some messages just give me some indiactations just like:</p>
                <ul>
                <li>http://127.0.0.1:5000/get/http</li>
                <li>http://127.0.0.1:5000/get/https</li>
                <li>http://127.0.0.1:5000/count/http</li>
                <li>http://127.0.0.1:5000/count/https</li>
                <li>http://127.0.0.1:5000/count/all</li>
                <ul>
            </div>
        </body>
    </html>
    """
    return web.Response(body=html.encode('utf-8'), content_type='text/html')


async def get_proxy(request):
    """
    get a proxy
    :param scheme: 指定要获取的代理的类型, http/https
    :return:
    """
    obj_redis = get_redis_connection()
    proxy = obj_redis.rpop_proxy(request.match_info.get('scheme', 'http'))
    return web.Response(text=str(proxy))


async def get_proxies_nums(request):
    """
    获取代理池中代理的数量
    :param scheme: 指定获取哪种（http/https)代理的可用数量，多给一个all选项
    :return:
    """
    obj_redis = get_redis_connection()
    scheme = request.match_info.get('scheme', 'all')
    if scheme == "all":
        nums_http = obj_redis.get_proxies_nums("http")
        nums_https = obj_redis.get_proxies_nums("https")
        nums_proxies = nums_http + nums_https
        return web.Response(text=str(nums_proxies))
    else:
        nums_proxies = obj_redis.get_proxies_nums(scheme)
        return web.Response(text=str(nums_proxies))


def main():
    app = web.Application()
    router = app.router
    router.add_get('/', index, name='index')
    router.add_get("/get/{scheme}", get_proxy, name='get_proxy')
    router.add_get("/count/{scheme}", get_proxies_nums, name='get_proxies_nums')
    web.run_app(app, host='0.0.0.0', port=1115)


if __name__ == '__main__':
    main()

