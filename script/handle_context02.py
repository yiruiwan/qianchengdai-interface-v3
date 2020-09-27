import re
from script.handle_sql import HandleMysql
from script.rebulit_config import HandleConfig,role_token
from script.path_split import USER_ACCOUNTS_FILE_PATH


do_mysql = HandleMysql()


class HandleContext:

    handle_config = HandleConfig(filename=USER_ACCOUNTS_FILE_PATH)  # 创建读取配置文件对象
    reg_pattern = re.compile(r'\$\{not_exited_tel\}')  # 编辑正则
    invest_pattern = re.compile(r'\$\{invest_user_tel\}')
    borrow_user_id_pattern = re.compile(r'\$\{borrow_user_id\}')
    borrow_user_not_id_pattern = re.compile(r'\$\{borrow_user_not_id\}')
    admin_user_tel_pattern = re.compile(r'\$\{admin_user_tel\}')
    loan_id_pattern = re.compile(r'\$\{loan_id\}')
    not_exit_id_pattern = re.compile(r'\$\{not_exited_loan_id\}')
    invest_user_id_pattern = re.compile(r'\$\{invest_user_id\}')
    borrow_user_tel = re.compile(r'\$\{borrow_user_tel\}')
    user_id = re.compile(r'\$\{user_id\}')



    @classmethod
    def create_not_exit_mobile_replace(cls,data):
        '''
        :param data: 注册接口传入的data
        :return: 将未注册的手机号替换原data中的patter
        '''

        do_mysql = HandleMysql()
        # 查找data数据中是否存在正则
        if re.search(cls.reg_pattern, data):
            # 生成新手机号
            new_mobile = do_mysql.creat_is_not_exit_mobile()
            # 替换正则
            data = re.sub(cls.reg_pattern, new_mobile, data)
        do_mysql.close()
        return data

    @classmethod
    def create_invest_mobile_replace(cls, data):
        '''
        :param data:注册接口传入的data
        :return:将未注册的手机号替换原data中的patter
        '''
        if re.search(cls.invest_pattern, data):
            new_mobile = str(cls.handle_config('invest_use', 'mobilephone'))
            data = re.sub(cls.invest_pattern, new_mobile, data)
        return data

    @classmethod
    def borrow_user_id_replace(cls, data):
        '''
        :param data:注册接口传入的data
        :return:将未注册的手机号替换原data中的patter
        '''
        if re.search(cls.borrow_user_id_pattern, data):
            new_id = str(cls.handle_config('borw_user', 'id'))
            data = re.sub(cls.borrow_user_id_pattern, new_id, data)
        return data

    @classmethod
    def borrow_user_not_id_replace(cls, data):
        '''
        替换不存在借款人id
        :param data:
        :return:
        '''
        sql = 'select max(Id) from member' # 查询最大的借款人id的sql
        id = do_mysql(sql=sql)  # 返回查询结果的字典
        new_id = id['max(Id)']+1  # 去字典key值+1
        # 查询到data中包含正则
        if re.search(cls.borrow_user_not_id_pattern, data):
            data = re.sub(cls.borrow_user_not_id_pattern, str(new_id), data)
        return data

    @classmethod
    def load_not_id_replace(cls, data):

        sql = 'select max(id) from loan'  # 查询最大的借款人id的sql
        id = do_mysql(sql=sql)  # 返回查询结果的字典
        new_id = id['max(id)'] + 1  # 去字典key值+1
        # 查询到data中包含正则
        if re.search(cls.not_exit_id_pattern, data):
            data = re.sub(cls.not_exit_id_pattern, str(new_id), data)
        return data

    @classmethod
    def admin_user_tel_replace(cls, data):
        '''
        :param data:注册接口传入的data
        :return:将未注册的手机号替换原data中的patter
        '''
        if re.search(cls.admin_user_tel_pattern, data):
            new_mobile = str(cls.handle_config('admin_user', 'mobilephone'))
            data = re.sub(cls.admin_user_tel_pattern, new_mobile, data)
        return data

    @classmethod
    def invest_user_tel_replace(cls, data):
        '''
        :param data:注册接口传入的data
        :return:将未注册的手机号替换原data中的patter
        '''
        if re.search(cls.invest_pattern, data):
            new_mobile = str(cls.handle_config('invest_use', 'mobilephone'))
            data = re.sub(cls.invest_pattern, new_mobile, data)
        return data

    @classmethod
    def borrow_user_tel_replace(cls, data):
        '''
        :param data:注册接口传入的data
        :return:将未注册的手机号替换原data中的patter
        '''
        if re.search(cls. borrow_user_tel, data):
            new_mobile = str(cls.handle_config('borw_user', 'mobilephone'))
            data = re.sub(cls. borrow_user_tel, new_mobile, data)
        return data

    @classmethod
    def invest_user_id_replace(cls, data):
        '''
        :param data:注册接口传入的data
        :return:将未注册的手机号替换原data中的patter
        '''
        if re.search(cls.invest_user_id_pattern, data):
            new_mobile = str(cls.handle_config('invest_use', 'id'))
            data = re.sub(cls.invest_user_id_pattern, new_mobile, data)
        return data

    @classmethod
    def order_system_user_id_replace(cls,data):
        '''
        :param data: 新增地址接口传入的data
        :return: 返回替换了用户id的url和data
        '''
        if re.search(cls.user_id, data):
            id = getattr(cls,"id")
            data = re.sub(cls.user_id, id, data)  # 注意sub的第二个参数为str类型
        return data

    @classmethod
    def addaddress_parma(cls,data):
        data = cls.order_system_user_id_replace(data)
        return data



    @classmethod
    def loan_replace(cls, data):
        if re.search(cls.loan_id_pattern, data):
            # 第一个参数为对象（类），第二个参数为字符类型的属性名
            # 获取这个对象（类）的实例属性值（类属性值）
            # setattr(对象, 字符类型的属性名, 属性值)
            # 类似于java中反射概念
            # cls.loan_id
            load_id = str(getattr(cls, "load_id"))
            data = re.sub(cls.loan_id_pattern, load_id, data)  # 第二个和第三个参数一定为字符串类型
        return data

    @classmethod
    def register_param(cls, data):
        # 替换未注册的手机号
        data = cls.create_not_exit_mobile_replace(data)
        # 替换注册的手机号
        data = cls.create_invest_mobile_replace(data)
        return data

    @classmethod
    def recharge_param(cls,data):

        pass

    @classmethod
    def add_param(cls, data):
        data = cls.admin_user_tel_replace(data)
        data = cls.borrow_user_id_replace(data)
        data = cls.borrow_user_not_id_replace(data)
        return data

    @classmethod
    def invest_param(cls, data):
        data = cls.admin_user_tel_replace(data)
        data = cls.invest_user_id_replace(data)
        data = cls.invest_user_tel_replace(data)
        data = cls.loan_replace(data)
        data = cls.load_not_id_replace(data)
        data = cls.borrow_user_id_replace(data)
        data = cls.borrow_user_tel_replace(data)
        return data


if __name__ == '__main__':
    handle_context = HandleContext()
    '''data1 = '{"mobilephone": "${not_exited_tel}", "pwd":"123456"}'
    data2 = '{"mobilephone": "${not_exited_tel}", "pwd":"123456", "regname": "KeYou"}'
    data3 = '{"mobilephone":"${invest_user_tel}","amount":600}'
    sql4 = '{"mobilephone":"${admin_user_tel}","pwd":"123456"}'''
    data5 = '{"mobilephone":"${invest_user_tel}","pwd":"123456"}'
    '''print(handle_context.invest_param(sql4))
    print(handle_context.register_param(data2))
    print(handle_context.register_param(data1))
    print(handle_context.register_param(data3))
    print(handle_context.add_param(sql4))'''
    # print(handle_context.register_param(data5))
    datas = 'SELECT mobile_phone FROM member WHERE mobile_phone =${not_exited_tel}'
    print(handle_context.register_param(datas))





