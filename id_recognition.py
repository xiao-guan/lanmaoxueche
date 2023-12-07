from pyunit_idcard import IdCard
from datetime import datetime as dt
from parseIdCard import parseIdCard


# 计算年龄并添加相应的年龄范围
def parseidcard(id, key):
    res = parseIdCard.parseIdCard(id)
    if res['code'] == 'Error':
        key_mapping = {
            'age': '出生日期',
            'gender': '性别',
            'area': '发证地'
        }
        card = IdCard()
        res = card.find_card(id)
        print(res)
        if key == 'age':
            # 将生日字符串转换为datetime对象
            birth_date = dt.strptime(res[key_mapping[key]], '%Y年%m月%d日')

            # 获取当前日期
            current_date = dt.now()

            # 计算年龄
            age = current_date.year - birth_date.year

            # 如果生日还没过，年龄需要减1
            if (current_date.month, current_date.day) < (birth_date.month, birth_date.day):
                age -= 1
            return age
        else:
            return res[key_mapping[key]]
    else:
        return res[key]


