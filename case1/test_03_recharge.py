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
# 导入路径拼接的模块
from script.path_split import DATA_PATH_FILE


read_excel = ReadExcel(sheet='recharge')  # 创建读取excel中recharge表单的对象
case = read_excel.get_case()  # 读取表单中的全部数据，返回嵌套字典的列表


@ddt
class TestRecharge(unittest.TestCase):
    # 模块开始时调用次方法
    @classmethod
    def setUpClass(cls):
        cls.open_request = HttpRequste()  # 创建处理request请求对象
        cls.do_sql = HandleMysql()  # 创建处理MySQL语句的对象
        do_log.info('开始执行充值用例')  # 日志文件中写入语句

    # 模块结束时调用次方法
    @classmethod
    def tearDownClass(cls):
        cls.open_request.close()  # 关闭处理request请求的对象
        cls.do_sql.close()  # 关闭处理MySQL语句的对象
        do_log.info('结束执行充值用例')  # 日志文件中写入语句

    @data(*case)
    def test_register(self, val):
        # 查看当前用例的名称
        # global recharge_before
        do_log.info("\nRunning Test Method: {}".format(inspect.stack()[0][3]))  # 监听器，显示当前执行的用例名称
        case_id = val['case_id']  # 获取excel中case_id行数据
        check_sql = val['check_sql']  # 获取excel中check_sql行数据
        # 判断如果check_sql行有数据
        if check_sql:
            # 将check_sql数据中参数化部分替换成配置文件中读取的数据
            check_sql = HandleContext().register_param(check_sql)
            # 调用MySQL模块的__call__方法，返回查询结果，字典类型
            sql = self.do_sql(sql=check_sql)
            # 读取返回结果中的LeaveAmount的值
            self.recharge_before = sql['LeaveAmount']
            self.recharge_before = float(round(self.recharge_before, 2))  # 金额为decimal类型，转换为float类型，并取二位小数
        # 拼接读取URL，配置文件中的+excel中的
        response_url = do_config('api', 'first_url')+val['url']
        # print(response_url)
        # 将data数据中参数化部分替换成配置文件中读取的数据
        new_data = HandleContext().register_param(val['data'])
        # 发送请求，返回请求json数据
        actual_result = self.open_request(method=val['method'],
                                          url=response_url,
                                          data=new_data)
        # 捕获异常，如果返回结果的status_code不是200，则抛出异常
        try:
            self.assertEqual(200, actual_result.status_code, msg='测试【{}】执行失败，状态码为【{}】'
                             .format(val['title'], actual_result.status_code))
        except AssertionError as e:
            do_log.error(e)
            raise e
        # 获取返回结果中code值
        # code = actual_result.json()['code']
        code = json.loads(actual_result.text).get('code')
        # 捕获异常，判断excel中expected值是否和返回的code值一致
        try:
            self.assertEqual(str(val['expected']), code)
            # 发送请求之后，再次通过sql语句，获取LeaveAmount值
            if check_sql:
                check_sql = HandleContext().register_param(check_sql)
                sql = self.do_sql(sql=check_sql)
                recharge_after = sql['LeaveAmount']  # 金额为decimal类型
                recharge_after = float(round(recharge_after, 2))
                amount = json.loads(new_data)['amount']  # 充值的金额
                # 期望结果
                except_amount = self.recharge_before + amount
                except_amount = round(except_amount, 2)
                self.assertEqual(except_amount, recharge_after)  # 断言期望结果与实际结果是否一致
        except AssertionError as e:  # 抛出异常
            do_log.error('抛出的异常为{}'.format(e))
            # 将不通过结果写入excel
            read_excel.write_case(row_number=case_id+1,
                                  finally_result=actual_result.text,
                                  result=do_config('excel', 'fail_result'))
            raise e
        else:
            # 将通过结果写入
            read_excel.write_case(row_number=case_id + 1,
                                  finally_result=actual_result.text,
                                  result=do_config('excel', 'pass_result'))


if __name__ == '__main__':

    unittest.main()