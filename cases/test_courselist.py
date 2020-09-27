import inspect
import unittest
from lib.ddt_20190803_174022 import data,ddt
# 导入处理读取excel中数据的模块
from script.do_excel import handle_aidong_excel
# 导入处理配置文件中数据的模块
from script.rebulit_config import do_config
from script.rebulit_log import do_log
from script.add_token_requests import token_request
from script.handle_aidong_context import HandleContext
from script.path_split import AIDONG_DATA_PATH_FILE


case = handle_aidong_excel.get_all_datas() # 读取所有excel中数据

@ddt
class TestCoures(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        do_log.info('开始执行获取课程列表用例')

    @classmethod
    def tearDownClass(cls):
        do_log.info('结束执行获取课程列表用例')

    @data(*case)
    def test_01_course(self,val):
        do_log.info("\nRunning Test Method: {}".format(inspect.stack()[0][3]))
        case_id = val['case_id']
        response_url = val['url']
        datas = val['data']
        method = val['method']
        # new_url = HandleContext().coures_msg(response_url)
        actual_result = token_request(method=method,url=response_url)
        '''if case_id == 1:
            id = (actual_result.json())['data']['course'][0]['id']
            HandleContext.id = id'''
        expect = val['expected']
        print(type(expect))
        code = actual_result.json()['status']
        try:
            self.assertEqual(expect,code)
        except:
            do_log.error('断言失败')
            handle_aidong_excel.write_datas(other_file=AIDONG_DATA_PATH_FILE,
                                            other_sheet='courselist',
                                            write_num=case_id + 1,
                                            actual_result=actual_result.text,
                                            result=do_config('excel', 'fail_result'))
            raise
        else:
            # 将通过结果写入
            handle_aidong_excel.write_datas(write_num=case_id + 1,
                                            other_file=AIDONG_DATA_PATH_FILE,
                                            other_sheet='courselist',
                                            actual_result=actual_result.text,
                                            result=do_config('excel', 'pass_result'))




