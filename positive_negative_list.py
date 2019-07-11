import numpy as np
import pandas as pd
import jieba
import jieba.analyse
import re


file_path = "D:\PythonCodes\Python_Course_Project/"

youyi = pd.read_csv("D:\PythonCodes\Python_Course_Project\youyi_precessed.csv")
fulihua = pd.read_csv("D:\PythonCodes\Python_Course_Project/fulihua_precessed.csv")
hilton = pd.read_csv("D:\PythonCodes\Python_Course_Project\hilton_precessed.csv")
kanglaide = pd.read_csv("D:\PythonCodes\Python_Course_Project\kanglaide_precessed.csv")
haitian_guoji = pd.read_csv("D:\PythonCodes\Python_Course_Project\haitianguoji_precessed.csv")
haijing = pd.read_csv("D:\PythonCodes\Python_Course_Project\haijing_precessed.csv")
weiduoliya = pd.read_csv("D:\PythonCodes\Python_Course_Project\weiduoliya_precessed.csv")
chuanbo_liwan =pd.read_csv("D:\PythonCodes\Python_Course_Project\chuanboliwan_precessed.csv")
liangyun = pd.read_csv("D:\PythonCodes\Python_Course_Project\liangyun_precessed.csv")
xianggelila = pd.read_csv("D:\PythonCodes\Python_Course_Project/xianggelila_precessed.csv")

# seg = jieba.cut(youyi['comments'][1])
# print('/'.join(seg))
# youyi_txt = ''
# for i in range(len(youyi)):
#     youyi_txt += str(youyi['comments'][i])
# # print(youyi_txt)
# seg = jieba.cut(youyi_txt)
# print('/'.join(seg))

# 进行正负样本的构建
# 评分大于4的判定为正样本

youyi = youyi.dropna()
youyi['class'] = youyi['avg_score'].map(lambda x: 1 if x >= 4 else 0)

fulihua = fulihua.dropna()
fulihua['class'] = fulihua['avg_score'].map(lambda x: 1 if x >= 4 else 0)

hilton = hilton.dropna()
hilton['class'] = hilton['avg_score'].map(lambda x: 1 if x >= 4 else 0)

kanglaide = kanglaide.dropna()
kanglaide['class'] = kanglaide['avg_score'].map(lambda x: 1 if x >= 4 else 0)

haitian_guoji = haitian_guoji.dropna()
haitian_guoji['class'] = haitian_guoji['avg_score'].map(lambda x: 1 if x >= 4 else 0)

haijing = haijing.dropna()
haijing['class'] = haijing['avg_score'].map(lambda x: 1 if x >= 4 else 0)

weiduoliya = weiduoliya.dropna()
weiduoliya['class'] = weiduoliya['avg_score'].map(lambda x: 1 if x >= 4 else 0)

chuanbo_liwan = chuanbo_liwan.dropna()
chuanbo_liwan['class'] = chuanbo_liwan['avg_score'].map(lambda x: 1 if x >= 4 else 0)

liangyun = liangyun.dropna()
liangyun['class'] = liangyun['avg_score'].map(lambda x: 1 if x >= 4 else 0)

xianggelila = xianggelila.dropna()
xianggelila['class'] = xianggelila['avg_score'].map(lambda x: 1 if x >= 4 else 0)


# 将正负样本分别保存
positive = pd.Series()
negative = pd.Series()
# positive = positive.append(youyi[youyi['class'] == 1]['comments'])
# negative = negative.append(youyi[youyi['class'] == 0]['comments'])
dataframe_list = [youyi, fulihua, hilton, kanglaide, haitian_guoji,
                  haijing, weiduoliya, chuanbo_liwan, liangyun, xianggelila]

for data in dataframe_list:
    positive = positive.append(data[data['class'] == 1]['comments'], ignore_index=True)
    negative = negative.append(data[data['class'] == 0]['comments'], ignore_index=True)

# print(positive.shape)
# print(negative.shape)
# print(type(positive))
# print(positive)
# print(negative)
positive.to_csv(file_path + 'positive.txt', index=False, sep='\t')
negative.to_csv(file_path + 'negative.txt', index=False, sep='\t')

