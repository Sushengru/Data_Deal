"""

对于知乎文章——《用pandas处理大数据——节省90%内存消耗的小贴士》的学习
https://zhuanlan.zhihu.com/p/28531346
"""

import pandas as pd
from pandas import DataFrame
import numpy as np

# 先生成df
df = DataFrame()


# 封装查询DF内存占用的方法
def mem_usage(pandas_object):
    if isinstance(pandas_object, pd.DataFrame):  # 先判断参数的类型是否为DF
        usage_B = pandas_object.memory_usage(deep=True).sum()  # 获取内存值

    else:  # 如果传入的是seri的话
        usage_B = pandas_object.memory_usage(deep=True)


# 1. 用info去获取DF的内存使用信息, memory_usage参数用于获取准确的内存占用值
df.info(memory_usage='deep')

# 2. 由于不同的数据类型是分开存放的，所以需要检查不同数据类型的平均内存占用
for dtype in ['float', 'int', 'object']:
    select_type = df.select_dtypes(include=[dtype])  # 快速选择某一数据类型的df数据
    mean_usage_B = select_type.memory_usage(deep=True).mean()  # 内存占用单位为B，还需要换算成MB
    mean_usage_MB = mean_usage_B / 1024 ** 2

    print("Average memory usage for {} columns: {:03.2f} MB".format(dtype, mean_usage_MB))

# 洞察不同数据类型的占用情况后，分类进行占用内存优化

# 3.优化数字型数据的内存占用——通过对子类型向下转化的形式减少内存占用
# 即将int64 转化为 uint8、uint32（unsigned int）
df_int = df.select_dtypes(include=['int'])
convert_int = df_int.apply(pd.to_numeric, downcast='unsigned')

# 4. 对浮点型数据进行同样的向下转化以减少内存占用, 即将float64转化为float32
df_folat = df.select_dtypes(include=['folat'])
convert_folat = df_folat.apply(pd.to_numeric, downcast='folat')

# 4. 优化字符串

# 4.1 对去重后数值个数极少的字符串，转化成类别型数据
# 首先需要对df中字符串数据类型进行洞察，确认unique数值个数
df_obj = df.select_dtypes(include=['obj'])
print(df_obj.describe())

# 对特定字段进行转变
df_n = df_obj.df_column_n
print(df_n.head())
df_category_n = df_n.astype('category')
print(df_category_n.head())
print(df_category_n.codes)  # 返回category用于表示字符串所用的数字


# 将数字型时间/日期转变成datetime,便于后续进行时间序列分析
date = df.date
df['date'] = pd.to_datetime(date, format='%Y%m%d')


# ------------------------------------------------------------------------
# 以上为优化内存占用的方式，那么如果能够在读取数据的时候就优化好数据是最好不过的了！
