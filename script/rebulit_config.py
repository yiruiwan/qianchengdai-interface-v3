import os
from configparser import ConfigParser
from script.path_split import CONFIG_PATH,USER_ACCOUNTS_FILE_PATH,CONFIG_PATH_FILE,CONFIG_TOKEN_PATH,API_TOKEN_PATH


class HandleConfig(ConfigParser):
    '''
    处理日志类
    '''

    def __init__(self,filename):
        super().__init__()  # 继承父类的构造方法
        self.config = filename

    def __call__(self, session='DEFAULT', option=None, is_bool=False, is_eval=False):
        self.read(self.config, encoding='utf8')

        if option is None:
            return dict(self[session])  # 返回default区块组成的字典

        if isinstance(is_bool, bool):
            if is_bool:
                self.getboolean(session, option)  # 返回指定区块下选项的值
        else:
            raise ValueError('不是bool值')
        data = self.get(session, option)

        if data.isdigit():
            return int(data)
        try:
            return float(data)
        except ValueError:

            pass

        if isinstance(is_eval, bool):
            if is_eval:
                return eval(data)
        else:
            raise ValueError('不是序列类型')
        return data

    @classmethod
    def write_config(cls, datas, filename):
        '''
        :param datas: 嵌套字典的字典
        :param filename: 需要写入配置文件的文件名
        '''
        config = cls(filename=filename)
        for key in datas:
            config[key] = datas[key]
        # filename = os.path.join(CONFIG_PATH,'filename')
        with open(filename, mode='w', encoding='utf-8')as file:
            config.write(file)


do_config = HandleConfig(CONFIG_PATH_FILE)
token_config = HandleConfig(CONFIG_TOKEN_PATH)
api_config = HandleConfig(API_TOKEN_PATH)
role_token = HandleConfig(USER_ACCOUNTS_FILE_PATH)
if __name__ == '__main__':

    #tokens = {"login_token":{"token": "c1233e37e912cda0b75d8ecc879ce8e6"},}
    #print(api_config.write_config(datas=tokens,filename=API_TOKEN_PATH))
    print(api_config('token','token'))


