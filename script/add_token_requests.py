import requests
import json
from script.rebulit_config import api_config, do_config
from script.get_token import request1


class TokenRequest:
    '''
    处理请求header中需要token的情况
    '''
    def __call__(self, method, url, data=None, is_json=False):
        '''

        :param method: 请求方法
        :param url: 请求url
        :param data: 请求数据
        :param is_json: 请求数据是否需要json数据
        :return: 请求结果
        '''
        login_url = do_config('api_data','login_url')  # 从config.ini配置文件中读取登录接口url
        # print(login_url)
        login_datas = do_config('api_data','datas')  # 从config.ini配置文件中读取登录接口data
        #  注意传入的参数为字典，所以配置文件中应该写成json格式，否则json.decoder.JSONDecodeError: Extra data: line 1 column 5 (char 4)
        # login_datas = json.loads(login_datas)
        # print(type(login_datas))
        request1.write_config(login_url=login_url,login_data=login_datas)  # 将登录接口获取到的token值写入到token_data.ini文件中
        user_tokens = api_config('token','token')  # 从token_data.ini文件中读取写入的token值
        # print(user_tokens)
        authorization_value = 'Bearer' + ' '+user_tokens
        # print(authorization_value)
        header = {'X-Lemonban-Media-Type':'lemonban.v2','Content-Type':'application/json','Authorization':authorization_value}
        # print(header)
        # print(type(user_tokens))
        method = method.lower()
        if isinstance(data, str):  # 判断输入的是否是字符串类型数据
            try:
                data = json.loads(data)  # 尝试转化为dict格式
            except Exception as e:
                data = eval(data)  # 转换为序列类型
        # 如果是get请求
        if method == "get":
            req = requests.get(url=url, params=data,headers= header)
            return req
        # 如果是post请求
        elif method == "post":
            # 如果data值需要是json类型
            if is_json:
                req = requests.post(url=url, json=data,headers=header)
                return req
            else:
                req = requests.post(url=url, data=data,headers=header)
                return req


token_request = TokenRequest()


if __name__ == '__main__':
    # 课程列表
    '''url='http://open.aidong.me/app/api/timetables'
    data = {"data":"2020-03-26","page":1,"mobile":13168717025}
    reqs=token_request(method='get',url=url,data=data)
    print(reqs.json()["data"]["timetable"][1]['id'])
    print(reqs.text)'''
    '''url = 'http://open.aidong.me/app/api/timetables/1019539'
    reqs = token_request(method='get',url=url)
    print(reqs.text)'''
    '''url = 'http://open.aidong.me/app/api/timetables'
    data = '{"data":"2020-03-26","page":1,"mobile":13168717025}'
    reqs = token_request(method='get', url=url, data=data)
    print(reqs.text)'''
    '''url1 = 'http://open.aidong.me/app/api/timetables/1'
    reqs = token_request(url=url1,method='get')
    print(reqs.text)
    url = 'http://open.aidong.me/app/api/timetables/1019540/coupons'
    data = '{"promotion_id":0,"quantity":1}'
    print(token_request(url=url, method='get',data=data ).text)
    url1= 'http://open.aidong.me/app/api/timetables/1019540/queue'
    data1 = '{"promotion_id":0,"quantity":1}'
    reqs = token_request(url=url1, method='post', data=data1)
    print(reqs.text)'''
    '''url2 ='http://a.aidong.me/market_home'
    data2= '{"page":1,"list":"market"}'
    reqs = token_request(url=url2, data=data2,method='get')
    print(reqs.text)
    good_id = reqs.json()["data"]["home"][0]["item"][2]['id']
    print(good_id)
    url3= 'http://a.aidong.me/market/products/nutrition/1245'
    reqs = token_request(url=url3,method='get')
    print(reqs.json())
    good_code = reqs.json()["data"]["product"]["spec"]["item"][0]["code"]
    print(good_code)
    url4 = 'http://a.aidong.me/mine/cart'
    data4 = '{"code": "pv4ld5-00yl-0001", "amount": 1}'
    reqs = token_request(url=url4,method='post',data=data4)
    print(reqs.json())
    url5 = 'http://a.aidong.me/market/products/nutrition/pv4ld5-00yl-0001}'
    data5 = '{"amount":1,"pay_type":"alipay","pick_up_way":0,"pick_up_id":4519,"is_food":0}'
    reqs = token_request(url=url4,method='post',data=data4)
    print(reqs.json())'''
    url = 'http://api.lemonban.com/futureloan/member/recharge'
    data = '{"member_id":8037625,"amount":99}'
    print(token_request(method='post',url=url,data=data,is_json=True).json())




