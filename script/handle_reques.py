import json
import requests


class HttpRequste:
    """
    封装request请求
    """
    def __init__(self):
        self.one_session = requests.Session()  # 创建会话，保存cookie值'''

    def __call__(self, method, url, data=None, is_json=False):
        '''
        :param method: 请求方法
        :param url: 请求地址
        :param data: 请求参数
        :param is_json: 判断请求参数是否是json格式
        :param kwargs: 可变参数，可串改user-agent
        :return: 返回请求数据
        '''

        method = method.lower()  # 将输入的请求方法转化为小写
        if isinstance(data, str):  # 判断输入的是否是字符串类型数据
            try:
                data = json.loads(data)  # 尝试转化为dict格式
            except Exception as e:
                data = eval(data)  # 转换为序列类型
        # header = {'X-Lemonban-Media-Type':'lemonban.v2','Content-Type':'application/json'}
        # 如果是get请求
        if method == "get":
            req = self.one_session.request( method='get',url=url, params=data)
        # 如果是post请求
        elif method == "post":
            # 如果data值需要是json类型
            if is_json:
                req = self.one_session.request(method='post',url=url, json=data)
            else:
                req = self.one_session.request(method='post',url=url, data=data)
        elif method == "delete":
            # 如果data值需要是json类型
            if is_json:
                req = self.one_session.request(method='delete', url=url, json=data)
            else:
                req = self.one_session.request(method='delete', url=url, data=data)
        else:
            req = None
            print("{}请求方式错误".format(method))
        return req

    def close(self):
        self.one_session.close()  # 关闭会话

    def add_headers(self, one_dict):
        """
        添加公共的请求头
        :param one_dict: 请求头参数，字典类型
        :return:
        """
        self.one_session.headers.update(one_dict)


if __name__ == '__main__':

    login_1 = HttpRequste()
    '''url='http://api.lemonban.com/futureloan/member/register'
    datas = '{"mobile_phone":"13168717011","pwd":"123456789"}'
    header = {"X-Lemonban-Media-Type":"lemonban.v2","Content-Type":"application/json"}
    login_1.add_headers(header)
    text = login_1(url=url,data=datas,method='post',is_json=True).json()
    print(text)'''
    url = 'http://127.0.0.1:8001/v2/login'
    datas = '{"username": "wyr","password": "1234567","captcha_code": "1234"}'
    print(login_1(url=url,data=datas,method='post').json())
    url1= 'http://127.0.0.1:8001/v1/users/1/addresses'
    datas1 = '{"user_id": "1","address": "福田下沙","address_detail": "下沙村","geohash": "31.22967, 121.4762","name": "小万","phone": "13168717023","tag": "12345","sex": 1,"phone_bk": "13168717023","tag_type": 2}'
    print((login_1(url=url1,data=datas1,method='post')).text)
























