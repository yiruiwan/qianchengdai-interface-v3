import requests
import json
from script.get_token import request1


class TokenRequest:
    '''
    处理请求header中需要token的情况
    '''
    def __call__(self, method, url, type=None,data=None, is_json=False, headers = None):
        '''
        :param method: 请求方法
        :param url: 请求url
        :param data: 请求数据
        :param is_json: 请求数据是否需要json数据
        :return: 请求结果
        '''
        method = method.lower()
        tokens = request1.get_token(type=type)
        authorization_value = 'Bearer' + ' '+tokens
        # print(authorization_value)
        header = {'X-Lemonban-Media-Type':'lemonban.v2','Content-Type':'application/json','Authorization':authorization_value}
        if isinstance(data, str):  # 判断输入的是否是字符串类型数据
            try:
                data = json.loads(data)  # 尝试转化为dict格式
            except Exception as e:
                data = eval(data)  # 转换为序列类型
        # 如果是get请求
        if method == "get":
            req = requests.get(url=url, params=data, headers=header)
            return req
        # 如果是post请求
        elif method == "post":
            # 如果data值需要是json类型
            if is_json:
                req = requests.post(url=url, json=data, headers=header)
                return req
            else:
                req = requests.post(url=url, data=data,headers=header)

                return req
        elif method == "patch":
            if is_json:
                req = requests.patch(url=url, json=data, headers=header)
                return req
            else:
                req = requests.patch(url=url, data=data, headers=header)

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

    '''url = 'http://api.lemonban.com/futureloan/member/recharge'
    data = '{"member_id":8067053,"amount":99}'
    text = token_request(method='Post',url=url,type='invest',data=data,is_json=True)'''

    url = 'http://api.lemonban.com/futureloan/loan/audit'
    data = {"loan_id":98908,"approved_or_not": "false"}
    print(type(data))
    text = token_request(method='patch',url=url,type='invest',is_json=True, data=data)
    print(text.json())



