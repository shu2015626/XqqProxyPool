from flask import Flask, g
from xqqproxypool.dboper.redis_oper import RedisOper

__all__ = ["app"]

app = Flask(__name__)

def get_redis_connection():
    """
    open a new redis connection if there is none
    yet for the current application context.
    :return:
    """
    if not hasattr(g, 'redis_client'):
        g.redis_client = RedisOper()
    return g.redis_client


@app.route("/")
def index():
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
    return html


@app.route("/get/<scheme>")
def get_proxy(scheme):
    """
    get a proxy
    :param scheme: 指定要获取的代理的类型, http/https
    :return:
    """
    obj_redis = get_redis_connection()
    proxy = obj_redis.rpop_proxy(scheme)
    return str(proxy)


@app.route("/count/<scheme>")
def get_proxies_nums(scheme):
    """
    获取代理池中代理的数量
    :param scheme: 指定获取哪种（http/https)代理的可用数量，多给一个all选项
    :return:
    """
    obj_redis = get_redis_connection()
    if scheme == "all":
        nums_http = obj_redis.get_proxies_nums("http")
        nums_https = obj_redis.get_proxies_nums("https")
        nums_proxies = nums_http + nums_https
        return str(nums_proxies)
    else:
        nums_proxies = obj_redis.get_proxies_nums(scheme)
        return str(nums_proxies)


if __name__ == '__main__':
    app.run()
