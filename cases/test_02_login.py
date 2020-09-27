import unittest
import inspect
import json
from lib.ddt_20190803_174022 import data,ddt
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


read_excel = ReadExcel(sheet='login')  # 创建读取excel中register表单的对象
case = read_excel.get_case()  # 读取表单中的全部数据，返回嵌套字典的列表


@ddt
class TestRegister(unittest.TestCase):
    # 模块开始时调用次方法
    @classmethod
    def setUpClass(cls):
        cls.open_request = HttpRequste()  # 创建处理request请求对象
        do_log.info('开始执行注册用例')  # 日志文件中写入语句

    # 模块结束时调用次方法
    @classmethod
    def tearDownClass(cls):
        cls.open_request.close()  # 关闭处理request请求的对象
        do_log.info('结束执行注册用例') # 日志文件中写入语句


    @data(*case)
    def test_register(self, val):
        # 查看当前用例的名称
        do_log.info("\nRunning Test Method: {}".format(inspect.stack()[0][3]))
        case_id = val['case_id']  # 获取excel中case_id行数据
        response_url = do_config('api', 'first_url')+val['url']   # 拼接读取URL，配置文件中的+excel中的
        # 将data数据中参数化部分替换成配置文件中读取的数据
        new_data = HandleContext().register_param(val['data'])
        # 发送请求，返回请求json数据
        actual_result = self.open_request(method=val['method'],
                                          url=response_url,
                                          data=new_data)
        # 捕获异常 判断excel中expected值是否和返回的code值一致
        try:
            self.assertEqual(val['expected'], actual_result.text)
        except AssertionError as e:
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
