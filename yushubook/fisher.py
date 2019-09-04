from app import create_app

__author__ = 'zhengpanone'
app = create_app()

print('id为' + str(id(app)) + '的app实例化')  # 查看内存地址
if __name__ == '__main__':
    print('id为' + str(id(app)) + '启动')
    app.run(host='0.0.0.0',port=8080, debug=True, threaded=True)
