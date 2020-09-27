import json

import requests


class HandleRequest:
    '''
    封装requests类
    '''

    def __init__(self):
        # 创建会话对象
        self.session = requests.Session()

    def send(self, method, url, **kwargs):
        """
        发送请求的方法
        :param method: 请求方法
        :param url: 请求url
        :param kwargs: headers请求头字典, data、json、files
        :return:
        """
        one_method = method.upper()

        kwargs["json"] = self.handle_param("json", kwargs)
        kwargs["data"] = self.handle_param("data", kwargs)

        return self.session.request(one_method, url, **kwargs)

    @staticmethod
    def handle_param(param_name, param_dict):

        if param_name in param_dict:
            data = param_dict.get(param_name)
            if isinstance(data, str):
                try:
                    data = json.loads(data)
                except Exception:
                    data = eval(data)

            return data
        # else:
        #     return None

    def add_headers(self, one_dict):
        """
        添加公共的请求头
        :param one_dict: 请求头参数，字典类型
        :return:
        """
        self.session.headers.update(one_dict)
        # self.session.headers = one_dict

    def close(self):
        """
        释放资源
        :return:
        """
        self.session.close()



if __name__ == '__main__':
    login_1 = HandleRequest()
    url = 'http://api.lemonban.com/futureloan/member/register'
    datas = '{"mobile_phone":"13168717012","pwd":"123456789"}'
    header = {"X-Lemonban-Media-Type": "lemonban.v2", "Content-Type": "application/json"}
    login_1.add_headers(header)
    text = login_1.send(url=url, json=datas, method='post').json()
    print(text)