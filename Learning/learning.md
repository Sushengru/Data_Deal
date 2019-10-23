## 记录这个项目模块里所用到的新知识和感想

### circulation_sql.py

    A. 认知和学习
        1. 首先是关于关于时间相关模块的认知， time、datetime、timeutil
        2. 其次是关于 timeutil模块中relativedelta函数，返回指定时间长度数值，可以用于时间的加减计算
        3. 再一次犯错并记住 ‘if __name__’ 中 __name__ 不需要加引号
        4. python常用生成日期/时间的方法之一：datetime.date() 和datetime.time()
        5. 关于pandas中如何去将多个df写入一个excel文件，新建 writer=pd.ExcelWriter(path) 对象，
            然后反复调用df.to_excel（writer，sheet_name), 最后save()
        6. pd.merge(df1, df2, on, letf_key, right_key)
        
    B. 感想
        1. 很久没有写过函数封装了，重新开始思考功能的封装步骤的实现确实有点费思考，这点多写之后应该就不是什么问题了
        2. 关于常用的封装有时间可以多写一点，便于自己去学习常用函数，以及扩宽一些思路
        3. 当前难度不大，后续期待有更大、更复杂的封装