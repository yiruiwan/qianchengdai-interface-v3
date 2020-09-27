import unittest
import inspect
from lib.ddt_20190803_174022 import ddt,data
# 导入处理读取excel中数据的模块
from script.do_excel import handle_new_api_invest
# 导入处理配置文件中数据的模块
from script.rebulit_config import do_config
# 导入处理sql查询语句的模块
from script.handle_sql import HandleMysql
# 导入处理log日志写入文件的模块
from script.rebulit_log import do_log
# 导入处理response请求的模块
from script.api_request import TokenRequest
# 导入正则参数化处理的模块
from script.handle_context02 import HandleContext
from script.path_split import NEW_API_DATA_PATH
case = handle_new_api_invest.get_all_datas()  # 读取表单中的全部数据，返回嵌套字典的列表
# print(case)


@ddt
class TestRegister(unittest.TestCase):
    # 模块开始时调用次方法
    @classmethod
    def setUpClass(cls):
        cls.open_request = TokenRequest()  # 创建处理request请求对象
        cls.handmysql = HandleMysql()
        do_log.info('开始执行充值用例')  # 日志文件中写入语句

    # 模块结束时调用次方法
    @classmethod
    def tearDownClass(cls):
        # cls.open_request.close()  # 关闭处理request请求的对象
        cls.handmysql.close()
        do_log.info('结束执行充值用例') # 日志文件中写入语句

    @data(*case)
    def test_invest(self,val):
        # 查看当前用例的名称
        do_log.info("\nRunning Test Method: {}".format(inspect.stack()[0][3]))
        case_id = val['case_id'] # 获取excel中case_id行数据
        response_url = val['url']
        method = val['method']
        type = val['type']
        check_sql = val['check_sql']
        # print(type)
        new_data = HandleContext().invest_param(val['data'])
        # 发送请求，返回请求json数据
        actual_result = self.open_request(method=method,
                                          url=response_url,
                                          data=new_data,
                                          is_json=True,
                                          type=type)
        #print(actual_result)

        code = actual_result.json()['code']

        # 捕获异常 判断excel中expected值是否和返回的code值一致
        try:
            self.assertEqual(200,actual_result.status_code,msg= '测试【{}】执行失败，状态码为【{}】'
                             .format(val['title'],actual_result.status_code))
        except AssertionError as e:
            do_log.error(e)
            raise e

        if check_sql:
            check_sql = HandleContext().invest_param(check_sql)
            id = self.handmysql(check_sql)
            HandleContext.load_id = id["id"]

        # 捕获异常，判断excel中expected值是否和返回的code值一致
        try:

            self.assertEqual(val['expected'],code)
        except Exception as e:
            do_log.error('抛出的异常为{}'.format(e))
            # 将不通过结果写入excel
            handle_new_api_invest.write_datas(other_file=NEW_API_DATA_PATH,
                                              other_sheet='invest',
                                              write_num=case_id + 1,
                                              actual_result=actual_result.text,
                                              result=do_config('excel', 'fail_result'))
            raise e
        else:
            # 将通过结果写入
            handle_new_api_invest.write_datas(other_file=NEW_API_DATA_PATH,
                                              other_sheet='invest',
                                              write_num=case_id + 1,
                                              actual_result=actual_result.text,
                                              result=do_config('excel', 'pass_result'))


if __name__ == '__main__':
    unittest.main()
