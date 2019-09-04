from urllib import request
import requests


# 发送http请求 urllib、requests
# scrapy ,requests + beautiful soap 爬虫
class HTTP:
    @staticmethod  # 静态方法
    def get(url, return_json=True):
        r = requests.get(url)
        # restful
        # json 三元表达式
        if r.status_code != 200:
            return {} if return_json else ''

        return r.json() if return_json else r.text

        '''
        if r.status_code == 200:
            if return_json:
                return r.json()
            else:
                return r.text
        else:
            if return_json:
            
                return {}
            else:
                return ''
        '''
