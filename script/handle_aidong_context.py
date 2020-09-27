import re


class HandleContext:
    course_pattern = re.compile(r'\$\{exit_id\}')
    good_code = re.compile(r'\$\{exit_code\}')

    @classmethod
    def id_replace(cls, data):
        if re.search(cls.course_pattern, data):
            # 第一个参数为对象（类），第二个参数为字符类型的属性名
            # 获取这个对象（类）的实例属性值（类属性值）
            # setattr(对象, 字符类型的属性名, 属性值)
            # 类似于java中反射概念
            # cls.loan_id
            id = str(getattr(cls, "id"))
            data = re.sub(cls.course_pattern, id, data)  # 第二个和第三个参数一定为字符串类型
        return data

    @classmethod
    def good_code_replace(cls, data):
        if re.search(cls.good_code, data):
            # 第一个参数为对象（类），第二个参数为字符类型的属性名
            # 获取这个对象（类）的实例属性值（类属性值）
            # setattr(对象, 字符类型的属性名, 属性值)
            # 类似于java中反射概念
            # cls.loan_id
            code_id = getattr(cls, "code_id")
            data = re.sub(cls.good_code, code_id, data)  # 第二个和第三个参数一定为字符串类型
        return data


    @classmethod
    def coures_details(cls,data):
        data = cls.id_replace(data)
        return data

    @classmethod
    def course_queue(cls,data):
        data = cls.id_replace(data)
        return data

    @classmethod
    def addcat(cls, data):
        data = cls.id_replace(data)
        data = cls.good_code_replace(data)
        return data


if __name__ == '__main__':
    handle_context = HandleContext()
    '''data = 'http://open.aidong.me/app/api/timetables/${exit_id}'
    print(handle_context.coures_details(data))'''
    datas = '{"code":"${exit_code}","amount":1}'
    print(handle_context.good_code_replace(datas))
    datas1 = 'http://a.aidong.me/market/products/nutrition/${exit_id}'
    print(handle_context.id_replace(datas1))
