import pymysql
import random
# 导入处理配置文件中数据的模块
from script.rebulit_config import do_config


class HandleMysql:
    '''
    读取mysql数据库类
    '''


    def __init__(self):
        '''
        初始化登录数据库操作
        '''
        self.conn = pymysql.connect(host = do_config('mysql','host'),
                                    user = do_config('mysql','user'),
                                    db = do_config('mysql','db'),
                                    password = str(do_config('mysql','password')),
                                    port = do_config('mysql','port'),
                                    charset = do_config('mysql','charset'),
                                    cursorclass = pymysql.cursors.DictCursor)
        self.cursor = self.conn.cursor() # 创建游标


    def __call__(self,sql,arg=None,is_more=False):
        self.cursor.execute(sql,arg) # 执行sql操作
        self.conn.commit() # 提交操作
        # 判断是否需要全部输出结果
        if is_more:
            res = self.cursor.fetchall()
        else:
            res = self.cursor.fetchone()
        return  res


# 随机获取手机号方法
    @staticmethod
    def get_mobilephone():
        '''
        :return: 返回一个随机的手机号码

        '''
        first_num =  ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
                        '150', '151', '152', '153', '155', '156', '157', '158', '159',
                        '180', '181', '182', '183', '184', '185', '186', '187', '188', '189']
        start_mobile = random.choice(first_num) # 随机选取列表中值
        num_str = '012345678'
        end_mobile = ''.join(random.sample(num_str,8))  # 随机从字符串中取8次
        new_mobile = start_mobile + end_mobile #拼接成一个手机号
        return new_mobile


    def is_exit_mobile(self,mobile):
        '''
        :return: # 判断数据库中是否存在随机生成的手机号
        '''
        data = 'SELECT * FROM member WHERE mobile_phone = %s'
        if  self(data,arg=(mobile,)): # 调用__call__方法
            return True
        else:
            return False

    def creat_is_not_exit_mobile(self):
        '''
        :return: 返回未注册的手机号码
        '''
        #循环判断随机生成的手机号码是否是之前数据库里面不存在的
        while True:
            mobile =self.get_mobilephone() # 调用随机生成的手机号函数，生成随机手机号
            if not self.is_exit_mobile(mobile):  # 如果手机号是之前数据库里面没有的循环停止，返回手机号
                break
        return mobile

    def close(self):

        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    handmysql = HandleMysql()
    '''sql1 = "SELECT * FROM member LIMIT 0,10"
    sql2 = 'SELECT * FROM member WHERE LeaveAmount>%s LIMIT 0,10'
    # print(handmysql(sql1,is_more =True))
    # print(handmysql(sql2,arg =(400,)))
    #sql = 'select max(Id) from member'
    sql = 'SELECT LeaveAmount FROM future.`member` WHERE MobilePhone = "13870889416"'
    #result =handmysql(sql2,arg=(4000,),is_more=True)
    #print(result[9])
    result = handmysql(sql)
    print(result)
    handmysql.close()'''
    '''sqls = "SELECT * FROM member where mobile_phone =%s"
    print(handmysql(sqls,arg=(13168717023,)))'''
    # print(HandleMysql().creat_is_not_exit_mobile())
    datas = 'SELECT mobile_phone FROM member WHERE mobile_phone =%s'
    mobile = '13168717023'
    result = handmysql(datas,arg=(mobile,))
    print(type(result))



