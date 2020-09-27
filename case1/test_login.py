import inspect
import unittest
import json
from lib.ddt_20190803_174022 import data,ddt
# 导入处理读取excel中数据的模块
from script.do_excel import handle_login_excel
# 导入处理配置文件中数据的模块
from script.rebulit_config import do_config
# 导入处理sql查询语句的模块
from script.handle_sql import HandleMysql
# 导入处理log日志写入文件的模块
from script.rebulit_log import do_log
from script.handle_reques import HttpRequste
from script.path_split import NEW_DATA_PATH_FILE

all_case = handle_login_excel.get_all_datas()   # 获取home表单中全部数据，返回嵌套字典的列表


@ddt
class TestLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.open_request = HttpRequste()  # 创建处理request请求对象
        do_log.info('开始执行注册用例')

    @classmethod
    def tearDownClass(cls):
        cls.open_request.close()
        do_log.info('结束执行用例')

    @data(*all_case)
    def test_login(self,val):
        # 查看当前用例的名称
        do_log.info("\nRunning Test Method: {}".format(inspect.stack()[0][3]))
        case_id = val['case_id']
        method = val['method']
        url = val['url']
        datas = val['data']
        expect = val['expected']
        expect = expect
        print(type(expect))
        actual_reqs = self.open_request(method=method, url=url, data=datas)
        actual = actual_reqs.text
        print(type(actual))
        try:
            self.assertEqual(val['expected'], actual)
        except AssertionError as e:
            do_log.error('抛出的异常为{}'.format(e))
            # 将不通过结果写入excel
            handle_login_excel.write_datas(other_file=NEW_DATA_PATH_FILE,
                                           other_sheet='login',
                                           write_num=case_id + 1,
                                           actual_result=actual,
                                           result='fail')
            raise e
        else:
            # 将通过结果写入
            handle_login_excel.write_datas(other_file=NEW_DATA_PATH_FILE,
                                           other_sheet='login',
                                           write_num=case_id + 1,
                                           actual_result=actual,
                                           result='ok')


if __name__ == '__main__':
    unittest.main()

