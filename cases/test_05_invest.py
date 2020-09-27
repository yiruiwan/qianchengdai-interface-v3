# -*- coding: utf-8 -*-
# file: test_03_recharge.py.py
# author:xiaoruirui
# time:2019/06/09
import unittest
import inspect
import json
from lib.ddt_20190803_174022 import ddt,data
# 导入处理读取excel中数据的模块
from script.rebulit_excel import ReadExcel
# 导入处理配置文件中数据的模块
from script.rebulit_config import do_config
# 导入处理sql查询语句的模块
from script.handle_sql import HandleMysql
# 导入处理log日志写入文件的模块
from script.rebulit_log import do_log
# 导入处理response请求的模块
from script.handle_reques import HttpRequste
# 导入正则参数化处理的模块
from script.handle_context02 import HandleContext
#导入路径拼接的模块
from script.path_split import DATA_PATH_FILE
from script.handle_context02 import HandleContext
readexcel = ReadExcel(sheet='invest') # 创建读取excel中recharge表单的对象
case = readexcel.get_case() # 读取表单中的全部数据，返回嵌套字典的列表
@ddt
class TestInvest(unittest.TestCase):
    # 模块开始时调用次方法
    @classmethod
    def setUpClass(cls):
        cls.open_request = HttpRequste() # 创建处理request请求对象
        cls.do_sql = HandleMysql()  # 创建处理MySQL语句的对象
        do_log.info('开始执行充值用例') # 日志文件中写入语句

    # 模块结束时调用次方法
    @classmethod
    def tearDownClass(cls):
        cls.open_request.close() # 关闭处理request请求的对象
        cls.do_sql.close() # 关闭处理MySQL语句的对象
        do_log.info('结束执行充值用例') # 日志文件中写入语句
    @data(*case)
    def test_register(self,val):
        # 查看当前用例的名称
        #global recharge_before
        do_log.info("\nRunning Test Method: {}".format(inspect.stack()[0][3])) # 监听器，显示当前执行的用例名称
        case_id =val['case_id'] # 获取excel中case_id行数据
        check_sql = val['check_sql'] # 获取excel中check_sql行数据
        response_url = do_config('api','first_url')+val['url']
        # print(response_url)
        # 将data数据中参数化部分替换成配置文件中读取的数据
        new_data = HandleContext().invest_param(val['data'])
        # 发送请求，返回请求json数据
        actual_result = self.open_request(method=val['method'],
                                          url=response_url,
                                          data=new_data)
        code = actual_result.json()['code']
        # 捕获异常，如果返回结果的status_code不是200，则抛出异常
        try:
            self.assertEqual(200,actual_result.status_code,msg= '测试【{}】执行失败，状态码为【{}】'
                             .format(val['title'],actual_result.status_code))
        except AssertionError as e:
            do_log.error(e)
            raise e
        if actual_result.json().get("msg")=='加标成功':
            if check_sql:
                check_sql= HandleContext().invest_param(check_sql)
                id = self.do_sql(check_sql)
                HandleContext.load_id = id["Id"]

        # 捕获异常，判断excel中expected值是否和返回的code值一致
        try:

            self.assertEqual(str(val['expected']),code)
        except AssertionError as e: # 抛出异常
            do_log.error('抛出的异常为{}'.format(e))
            # 将不通过结果写入excel
            readexcel.write_case(row_number = case_id+1,
                                 finally_result=actual_result.text,
                                 result=do_config('excel','fail_result'))
            raise e
        else:
            # 将通过结果写入
            readexcel.write_case(row_number=case_id + 1,
                                 finally_result=actual_result.text,
                                 result=do_config('excel','pass_result'))


if __name__ == '__main__':
    unittest.main()