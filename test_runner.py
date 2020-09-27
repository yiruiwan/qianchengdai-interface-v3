import unittest
import os
from datetime import datetime
from lib import HTMLTestRunnerNew
from script.rebulit_config import do_config
from script.path_split import REPORT_PATH,USER_ACCOUNTS_FILE_PATH,CASES_PATH
from script.create_user import generate_new_user
if not USER_ACCOUNTS_FILE_PATH:
    generate_new_user()
# one_load = unittest.TestLoader()
# one_suit = unittest.TestSuite(tests=one_tuple)
one_suit = unittest.defaultTestLoader.discover(CASES_PATH)
report_name = os.path.join(REPORT_PATH,do_config('report','report_html_name'))
report_full_name = report_name+ '-'+ datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")+ '.html'
with open(report_full_name,mode='wb')as filename:
    one_run = HTMLTestRunnerNew.HTMLTestRunner(stream=filename,
                                               verbosity=2,tester='wyr',
                                               title='测试用例')
    one_run.run(one_suit)


