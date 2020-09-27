# -*- coding: utf-8 -*-
# file: create_user.py
# author:xiaoruirui
# time:2019/06/08
# 导入处理response请求的模块


from script.handle_reques import HttpRequste
# 导入处理sql查询语句的模块
from script.handle_sql import HandleMysql
# 导入处理配置文件中数据的模块
from script.rebulit_config import do_config
#  导入路径拼接的模块
from script.path_split import USER_ACCOUNTS_FILE_PATH


# 创建手机号写入配置文件
def create_user(reg_name,type,pwd='12345678'):
        do_request = HttpRequste()
        do_mysql = HandleMysql()
        global user_id
        sql = 'SELECT id from member where mobile_phone = %s'
        response_url = 'http://api.lemonban.com/futureloan/member/register'
        while True:
            new_mobile = do_mysql.creat_is_not_exit_mobile() # 获取一个新的手机号
            # print(new_mobile)
            header = {"X-Lemonban-Media-Type":"lemonban.v2","Content-Type":"application/json"}
            do_request.add_headers(header)
            data = {"mobile_phone": new_mobile, "pwd": pwd,'reg_name':reg_name,"type":type} # 传入接口的请求data
            # print(data)
            response = do_request(method='post',
                                  url=response_url,
                                  data=data,
                                  is_json=True)  # 获取一个新手机号去注册接口跑一下，获取响应数据，
            # print(response.json())
            # 因为注册成功后在数据库里面传入一个新的记录
            result = do_mysql(sql=sql, arg=(new_mobile,))  # 去数据库里面查询手机号码是否存在
            # print(result)
            if result:
                 user_id = result['id'] # 获取用户Id
                 break
        # 将获取到Id、手机号码、 密码等创建成一个字典，方便调用处理配置文件中的写入方法
        new_dict = {reg_name:{"id":user_id,"reg_name":reg_name,"pwd":pwd,"mobilephone":new_mobile}}
        do_mysql.close()
        return new_dict


def generate_new_user():
    new_data_dict ={}
    new_data_dict.update(create_user(reg_name="admin_user",type=1)) # 字典增加值
    new_data_dict.update(create_user(reg_name="borw_user",type=0))
    new_data_dict.update(create_user(reg_name="invest_use",type=0))
    do_config.write_config(filename=USER_ACCOUNTS_FILE_PATH,datas=new_data_dict)  # 调用处理配置文件写入方法


if __name__ == '__main__':
    generate_new_user()
