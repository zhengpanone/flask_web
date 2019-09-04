from flask import Flask, make_response

# from config import DEBUG #通过模块读取配置文件
__author__ = 'zhengpanone'

app = Flask(__name__)
app.config.from_object('config')  # fun1 载入配置文件

print(app.config['DEBUG'])  # DEBUG默认值False


# print(app.config['Debug'])  # config必须大写


# 重定向/hello  ==> /hello/
@app.route('/hello/')  # 装饰器最后调用的 add_url_rule()这个方法
def hello():
    return 'Hello Flask!'


def helloflask():
    # 基于类的视图(即插视图) 必须使用 add_url_rule()来注册路径
    return 'Hello Flask'


app.add_url_rule('/helloflask', view_func=helloflask)


@app.route('/lesson02')
def lesson02():
    # status code
    # content-type http headers
    # 默认值 content-type = text/html
    # Response
    headers = {
        'content-type': 'text/plain'
    }
    response = make_response('<html></html>', 404)
    response.headers = headers
    return response


# 重定向
@app.route('/lesson03')
def lesson03():
    # 'content-type':'application/json'
    headers = {
        'content-type': 'text/plain',
        'location': 'http://www.bing.com'
    }
    response = make_response('<html></html>', 301)
    response.headers = headers
    return response


@app.route('/lesson04')
def lesson04():
    headers = {
        'content-type': 'application/json'
    }
    response = make_response('{username:zhengpan,password:test}', 301)
    response.headers = headers
    return response


@app.route('/lesson05')
def lesson05():
    headers = {
        'content-type': 'application/json',
    }
    return '<html></html>', 301, headers  # 返回的是元组


if __name__ == '__main__':  # 确保下面的方法只在入口文件执行 确保生产环境启用的不是flask自带的服务器
    # 生产环境 nginx+uwsgi 生产环境uwsgi加载模块,模块不再是入口文件
    # config 是字典dict的子类
    app.run(host='10.10.100.2', port=8180, debug=app.config['DEBUG'])  # host指定端口号 host = '0.0.0.0'可以外网访问
