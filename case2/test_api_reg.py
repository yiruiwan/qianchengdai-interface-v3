import unittest
import inspect
import json
from lib.ddt_20190803_174022 import ddt,data
# 导入处理读取excel中数据的模块
from script.do_excel import handle_new_api_reg
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
from script.path_split import NEW_API_DATA_PATH
case = handle_new_api_reg.get_all_datas()  # 读取表单中的全部数据，返回嵌套字典的列表
print(case)



@ddt
class TestRegister(unittest.TestCase):
    # 模块开始时调用次方法
    @classmethod
    def setUpClass(cls):
        cls.open_request = HttpRequste()  # 创建处理request请求对象
        cls.handmysql = HandleMysql()
        do_log.info('开始执行注册用例')  # 日志文件中写入语句

    # 模块结束时调用次方法
    @classmethod
    def tearDownClass(cls):
        cls.open_request.close()
        cls.handmysql.close()
        do_log.info('结束执行注册用例') # 日志文件中写入语句

    @data(*case)
    def test_reg(self,val):
        self.open_request.add_headers(eval(do_config('headers', 'headers')))
        # 查看当前用例的名称
        do_log.info("\nRunning Test Method: {}".format(inspect.stack()[0][3]))
        case_id = val['case_id'] # 获取excel中case_id行数据
        # response_url = do_config('api','first_url')+val['url']   # 拼接读取URL，配置文件中的+excel中的
        response_url = val['url']
        # check_sql = val['check_sql']
        # 将data数据中参数化部分替换成配置文件中读取的数据
        new_data = HandleContext().register_param(val['data'])
        # print(type(new_data))
        mobile = eval(new_data)['mobile_phone']
        print(type(mobile))
        # 发送请求，返回请求json数据
        actual_result = self.open_request(method=val['method'],
                                          url=response_url,
                                          data=new_data,
                                          is_json=True)

        code = actual_result.json()['code']
        # 捕获异常 判断excel中expected值是否和返回的code值一致
        try:
            self.assertEqual(val['expected'], code)
        except AssertionError as e:
            do_log.error('抛出的异常为{}'.format(e))
            # 将不通过结果写入excel
            handle_new_api_reg.write_datas(other_file=NEW_API_DATA_PATH,
                                           other_sheet='reg',
                                           write_num=case_id + 1,
                                           actual_result=actual_result.text,
                                           result=do_config('excel', 'fail_result'))
            raise e
        else:
            # 将通过结果写入
            handle_new_api_reg.write_datas(other_file=NEW_API_DATA_PATH,
                                           other_sheet='reg',
                                           write_num=case_id + 1,
                                           actual_result=actual_result.text,
                                           result=do_config('excel', 'pass_result'))


if __name__ == '__main__':

    unittest.main()