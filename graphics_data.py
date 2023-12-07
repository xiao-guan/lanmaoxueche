import pandas as pd

# 读取CSV文件
data = pd.read_csv('unique_data.csv')

# 去除重复身份证号的数据，保留唯一的身份证号
data_unique = data.drop_duplicates(subset='identityNumber', keep='first')

# 将处理后的数据重新写入新的CSV文件
data_unique.to_csv('unique_identity_numbers.csv', index=False)
