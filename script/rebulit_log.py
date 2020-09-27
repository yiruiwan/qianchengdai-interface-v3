import logging
from logging.handlers import RotatingFileHandler
from script.rebulit_config import do_config
from script.path_split import LOG_PATH_FILE


class HandleLog:
    '''
    处理log日志类
    '''
    def __init__(self):
        # 创建一个case_log日志器
        self.case_log = logging.getLogger(do_config('log','log_name'))
        # 设置日志器的等级
        self.case_log.setLevel(do_config('log','log_level'))
        # 设置日志输出平台
        file_handle = RotatingFileHandler(filename=LOG_PATH_FILE,
                                          maxBytes=do_config('log','max_byte'),
                                          backupCount=do_config('log','backup_count'),
                                          encoding='utf-8')
        # 设置输出平台展示日志的等级
        file_handle.setLevel(do_config('log','file_handle_level'))
        # 日志展示格式
        vebor_formatter = logging.Formatter(do_config('log','handle_formate'))
        # 平台添加日志展示格式
        file_handle.setFormatter(vebor_formatter)
        # 日志器添加到平台
        self.case_log.addHandler(file_handle)

    def get_case(self):
        '''
        :return: 日志器
        '''
        return self.case_log


do_log = HandleLog().get_case()
if __name__ == '__main__':
    case_log =HandleLog().get_case()

    case_log.info('infor')
    case_log.debug('debug')
    case_log.error('error')
