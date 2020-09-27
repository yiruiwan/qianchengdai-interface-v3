import unittest
import inspect
import json
from lib.ddt_20190803_174022 import ddt, data
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
# 导入路径拼接的模块
from script.path_split import DATA_PATH_FILE


read_excel = ReadExcel(sheet='recharge')  # 创建读取excel中recharge表单的对象
case = read_excel.get_case()   # 读取表单中的全部数据，返回嵌套字典的列表
# print(case)


@ddt
class TestRecharge01(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.requests = HttpRequste()
        cls.do_sql = HandleMysql()
        do_log.info("充值用例开始执行")

    @classmethod
    def tearDownClass(cls):
        cls.requests.close()
        cls.do_sql.close()
        do_log.info("充值用例执行结束")

    @data(*case)
    def test_recharge(self, val):
        do_log.info("\nRunning Test Method: {}".format(inspect.stack()[0][3]))  # 监听器，显示当前执行的用例名称
        response_url = do_config('api', 'first_url') + val['url']
        case_id = val["case_id"]
        check_sql = val["check_sql"]
        # sql = HandleContext.register_param(check_sql)
        # print(sql)
        if check_sql:
            sql = HandleContext.register_param(check_sql)
            sql_text = self.do_sql(sql=sql)
            recharge_before_amount = sql_text["LeaveAmount"]
            self.recharge_before_amount = float(round(recharge_before_amount, 2))
            print(self.recharge_before_amount)
        response_data = val["data"]
        response_data = HandleContext().register_param(response_data)
        print(type(response_data))
        method = val["method"]
        response_url = do_config('api', 'first_url') + val['url']
        response = self.requests(method=method, url=response_url, data=response_data)
        print(response.text)
        try:
            self.assertEqual(200, response.status_code)
        except Exception as e:
            do_log.error("请求失败")
            raise e

        expected = val["expected"]
        code = response.json()["code"]
        try:
            self.assertEqual(str(val['expected']), code)
            if check_sql:
                sql = HandleContext.register_param(check_sql)
                sql_text = self.do_sql(sql=sql)
                recharge_after_amount = sql_text["LeaveAmount"]
                recharge_after_amount = float(round(recharge_after_amount, 2))
                # print(recharge_after_amount)
                amount = eval(response_data)["amount"]
                # print(eval(response_data)["amount"])
                actual_amount = self.recharge_before_amount + amount
                actual_amount = round(actual_amount, 2)
                # print(actual_amount)
                self.assertEqual(actual_amount, recharge_after_amount)
        except AssertionError as e:
            do_log.error('抛出的异常为{}'.format(e))
            # 将不通过结果写入excel
            read_excel.write_case(row_number=case_id+1,
                                  finally_result=code,
                                  result=do_config('excel', 'fail_result'))
            raise e
        else:
            # 将通过结果写入
            read_excel.write_case(row_number=case_id + 1,
                                  finally_result=code,
                                  result=do_config('excel', 'pass_result'))


if __name__ == '__main__':
    unittest.main()






