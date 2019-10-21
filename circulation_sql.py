"""
目的： 实现循环查询某个sql

"""
from DB_Connect import db_connect
import pandas as pd
from pandas import DataFrame
import datetime  # 获取日期
from dateutil.relativedelta import relativedelta  # 实现日期做差


# 按月实现新老客、累计老客的循环查询sql
def store_sql(start_date, end_date, if_limit=1):

    if if_limit == 1:

        # 需要一个参数，将时间减去2年
        date_diff = start_date - relativedelta(years=2)

        # 按月计算每月 近2年老客复购人数
        repurchase = """SELECT DATE_FORMAT( pay_time, '%%Y-%%m') AS the_date, count( DISTINCT buyer_nick ) FROM triumph 
                            WHERE pay_time >= "{}" AND pay_time < "{}"  
                            AND buyer_nick IN (select buyer_nick from triumph_stat 
                                            where first_purchase_time < "{}" and first_purchase_time >= "{}" )
                            GROUP BY the_date""".format(start_date, end_date, start_date, )

        # 累计近2年老客人数
        customer = """select DATE_FORMAT("{}", '%%Y-%%m') AS the_date, count(distinct buyer_nick) from triumph_stat 
                            where first_purchase_time <"{}" 
                            and first_purchase_time > "{}" """.format(start_date, start_date, date_diff)
    else:
        # 按月计算每月老客人数
        repurchase = """SELECT DATE_FORMAT( pay_time, '%%Y-%%m') AS the_date, count( DISTINCT buyer_nick ) FROM triumph 
                            WHERE pay_time >= "{}" AND pay_time < "{}"  
                            AND buyer_nick IN (select buyer_nick from triumph_stat 
                                            where first_purchase_time < "{}" )
                            GROUP BY the_date""".format(start_date, end_date, start_date)

        # 累计老客人数
        customer = """select DATE_FORMAT("{}", '%%Y-%%m') AS the_date, count(distinct buyer_nick) from triumph_stat 
                            where first_purchase_time <"{}" """.format(start_date, start_date)

    return repurchase, customer


if __name__ == '__main__':

    # 需要查询的品牌名称,用英文
    brand_name = 'triumph'

    # 是否需要限定在2年内的老客,用于sql的选择
    # 0为不限定，1为限定
    if_limited = 0

    # 开始日期
    s_date = datetime.date(2015, 1, 1)
    e_date = datetime.date(2015, 2, 1)

    # last_date用于计算月份差， 以确定for循环次数
    last_date = datetime.date(2019, 10, 1)

    """
    以上为需要修改的参数
    --------------------------------------------------------------------------------------------
    以下为运行参数和具体执行代码
    """

    # 输出文件名称
    excel_name = brand_name + r'复购和老客数据.xlsx'

    # 计算循环次数
    month_diff = abs((last_date.year - s_date.year) * 12 + (last_date.month - s_date.month) * 1)
    print(s_date, last_date, month_diff)

    # 调用数据库接口
    db_brand = db_connect.db_brand()

    # 新建2个空的df， 用于concat
    repurchase_trend = DataFrame()
    customer_trend = DataFrame()

    for i in range(month_diff):
        # 获取按月循环执行的sql
        repurchases, customers = store_sql(s_date, e_date, if_limit=if_limited)
        print(repurchases, customers)

        df_repurchases = pd.read_sql(repurchases, con=db_brand)
        df_customers = pd.read_sql(customers, con=db_brand)

        # 需要重新定义下df的列名
        df_repurchases.columns = ['日期', '老客人数']
        df_customers.columns = ['日期', '累计老客数']

        # 用定义的空df来concat循环查询结果
        repurchase_trend = pd.concat([repurchase_trend, df_repurchases], axis=0)
        customer_trend = pd.concat([customer_trend, df_customers], axis=0)

        # 迭代日期
        s_date = s_date + relativedelta(months=1)
        e_date = e_date + relativedelta(months=1)
        print(s_date, e_date)

    data = pd.merge(repurchase_trend, customer_trend, how='left', left_on=['日期'], right_on=['日期'])

    file_path = 'Doc/' + excel_name
    writer = pd.ExcelWriter(file_path)
    data.to_excel(writer, r'复购数据')
    writer.save()
