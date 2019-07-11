import numpy as np
import pandas as pd
import csv


def drop_comment_below4(data, columns='comments'):
    """
    去掉缺失值
    去掉重复的评论
    去掉评论少于四个字的评论
    :param data: 数据
    :param columns: 需要判断的列
    :return:返回处理后的结果
    """

    data = data.drop_duplicates(subset=columns)
    index_list = data[data[columns].str.len() <= 4].index.tolist()
    data_clean = data.drop(index=index_list)

    return data_clean


youyi = pd.read_csv("D:\PythonCodes\Python_Course_Project\youyi.csv")
fulihua = pd.read_csv("D:\PythonCodes\Python_Course_Project/fulihua.csv")
hilton = pd.read_csv("D:\PythonCodes\Python_Course_Project\hilton.csv")
kanglaide = pd.read_csv("D:\PythonCodes\Python_Course_Project\kanglaide.csv")
haitian_guoji = pd.read_csv("D:\PythonCodes\Python_Course_Project\haitianguoji.csv", encoding='utf_8_sig')
haijing = pd.read_csv("D:\PythonCodes\Python_Course_Project\haijing.csv")
weiduoliya = pd.read_csv("D:\PythonCodes\Python_Course_Project\weiduoliya.csv")
chuanbo_liwan = pd.read_csv("D:\PythonCodes\Python_Course_Project\chuanboliwan.csv")
liangyun = pd.read_csv("D:\PythonCodes\Python_Course_Project\liangyun.csv")
xianggelila = pd.read_csv("D:\PythonCodes\Python_Course_Project/xianggelila.csv")

print(hilton.iloc[1, :])
# youyi = youyi.drop_duplicates(subset='comments')
# fulihua = fulihua.drop_duplicates(subset='comments')
# hilton = hilton.drop_duplicates(subset='comments')
# kanglaide = kanglaide.drop_duplicates(subset='comments')
# haitian_guoji = haitian_guoji.drop_duplicates(subset='comments')
# haijing = haijing.drop_duplicates(subset='comments')
# weiduoliya = weiduoliya.drop_duplicates(subset='comments')
# chuanbo_liwan = chuanbo_liwan.drop_duplicates(subset='comments')
# liangyun = liangyun.drop_duplicates(subset='comments')
# xianggelila = xianggelila.drop_duplicates(subset='comments')


youyi = drop_comment_below4(youyi, 'comments')
fulihua = drop_comment_below4(fulihua, 'comments')
hilton = drop_comment_below4(hilton, 'comments')
kanglaide = drop_comment_below4(kanglaide, 'comments')
haitian_guoji = drop_comment_below4(haitian_guoji, 'comments')
haijing = drop_comment_below4(haijing, 'comments')
weiduoliya = drop_comment_below4(weiduoliya, 'comments')
chuanbo_liwan = drop_comment_below4(chuanbo_liwan, 'comments')
liangyun = drop_comment_below4(liangyun, 'comments')
xianggelila = drop_comment_below4(xianggelila, 'comments')

print(haitian_guoji.iloc[1, :])

youyi.to_csv("D:\PythonCodes\Python_Course_Project\youyi_precessed.csv", index=False)
fulihua.to_csv("D:\PythonCodes\Python_Course_Project/fulihua_precessed.csv", index=False)
hilton.to_csv("D:\PythonCodes\Python_Course_Project\hilton_precessed.csv", index=False)
kanglaide.to_csv("D:\PythonCodes\Python_Course_Project\kanglaide_precessed.csv", index=False)
haitian_guoji.to_csv("D:\PythonCodes\Python_Course_Project\haitianguoji_precessed.csv", index=False)
haijing.to_csv("D:\PythonCodes\Python_Course_Project\haijing_precessed.csv", index=False)
weiduoliya.to_csv("D:\PythonCodes\Python_Course_Project\weiduoliya_precessed.csv", index=False)
chuanbo_liwan.to_csv("D:\PythonCodes\Python_Course_Project\chuanboliwan_precessed.csv", index=False)
liangyun.to_csv("D:\PythonCodes\Python_Course_Project\liangyun_precessed.csv", index=False)
xianggelila.to_csv("D:\PythonCodes\Python_Course_Project/xianggelila_precessed.csv", index=False)
