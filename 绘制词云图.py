import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame
import csv
import jieba
import jieba.analyse
import codecs
import wordcloud
import nltk
import re
import jieba.posseg as psg
import jieba.analyse
import matplotlib.pyplot as plt
import pickle
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

file_path = "D:\PythonCodes\Python_Course_Project/"

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

summary = [kanglaide, hilton, liangyun, chuanbo_liwan, haitian_guoji, haijing, youyi, xianggelila, fulihua, weiduoliya]
# print(kanglaide.columns)

# 把分数装在一个列表中
l1 = []
for i in summary:
    li = [i for i in i.scores.str.split("，")]
    l1.extend(li)
# 四个空列表，预备装四个方面的分数
l3 = []
l4 = []
l5 = []
l6 = []
# 得到分离出来的四个方面的分数
for j in l1:
    l2 = [x for x in j[0].split(',')]
    lw = int(l2[0][-3])
    ls = int(l2[1][-3])
    lf = int(l2[2][-3])
    ls = int(l2[3][-3])
    l3.append(lw)  #
    l4.append(ls)
    l5.append(lf)
    l6.append(ls)
print(l3)
# 求四个方面分数的平均值
mean1 = sum(l3) / len(l3)
print(mean1)
mean2 = sum(l4) / len(l4)
print(mean2)
mean3 = sum(l5) / len(l5)
print(mean3)
mean4 = sum(l6) / len(l6)
print(mean4)

# 去除长度小于4的评论
for i in summary:
    i[i.avg_score > 4].shape[0]  # 评论小于4
    l1 = i[i.avg_score > 4].index
    l2 = i[i.avg_score.isnull()].index
    i.drop(l1, inplace=True)
    i.drop(l2, inplace=True)


# 只匹配评论中的汉字和标点符号
def clean_data(text):
    pattern = re.compile('[\u4e00-\u9fa5]|[\（\）\《\》\——\；\，\。\“\”\<\>\！]')  # 只匹配标点符号和中文
    res = pattern.findall(text)
    res = ''.join(res)
    return res


for i in summary:
    i.comments = i.comments.astype('str')
    i['comments'] = i['comments'].apply(clean_data)
    i.head()


def cut_words(i, summary):
    """
    进行分词
    """

    b = ""
    #     filepath="D://"+str(i)+".txt"
    text = summary[i].comments.astype('str')
    for j in text:
        words = jieba.lcut(j)
        words = " ".join(words)
        words = "\n" + words
        #         with open(filepath,"a",encoding="utf_8_sig") as f:
        #             f.write(words)
        b += words
    return b


# 分词
kang_cxbz = cut_words(0, summary)
dun_cxbz = cut_words(1, summary)
yun_cxbz = cut_words(2, summary)
wan_cxbz = cut_words(3, summary)
tian_cxbz = cut_words(4, summary)
jing_cxbz = cut_words(5, summary)
you_cxbz = cut_words(6, summary)
xiang_cxbz = cut_words(7, summary)
hua_cxbz = cut_words(8, summary)
wei_cxbz = cut_words(9, summary)


# 将分词结果转化为列表
def llist(object):
    """
    将结果转换成列表，利于后续操作
    """
    llist = [i for i in object.split(' ')]
    return llist


kang_list = llist(kang_cxbz)
dun_list = llist(dun_cxbz)
yun_list = llist(yun_cxbz)
wan_list = llist(wan_cxbz)
tian_list = llist(tian_cxbz)
jing_list = llist(jing_cxbz)
you_list = llist(you_cxbz)
xiang_list = llist(xiang_cxbz)
hua_list = llist(hua_cxbz)
wei_list = llist(wei_cxbz)
textlist = [kang_list, dun_list, yun_list, wan_list, tian_list, jing_list, you_list, xiang_list, xiang_list, hua_list,
            wei_list]


def stopwordslist():
    """停用词列表"""
    stopwords = [line.strip() for line in open("D://stopWord.txt", encoding="utf_8_sig").readlines()]
    stopwords.extend(['大连', '酒店', '宾馆', '康莱德', '希尔德', '友谊', '希尔顿', '良运', '香格里拉', '维多利亚', '船舶丽湾'])
    return stopwords


stopwords = stopwordslist()


def stop_word(textlist):
    """
    去除停用词
    """
    li = []
    for i in textlist:
        if i not in stopwords:
            li.append(i)
        else:
            continue
    return li


for i in textlist:
    i = stop_word(i)
# 绿色酒店与非绿色酒店去除停用词结果
green = textlist[:5]
gray = textlist[5:10]

# 将列表转化为字符串
kk = " ".join(textlist[0])
dd = " ".join(textlist[1])
yy = " ".join(textlist[2])
ww = " ".join(textlist[3])
tt = " ".join(textlist[4])
jj = " ".join(textlist[5])
uu = " ".join(textlist[6])
xx = " ".join(textlist[7])
hh = " ".join(textlist[8])
vv = " ".join(textlist[9])
green_tol = [kk, dd, yy, ww, tt]
gray_tol = [jj, uu, xx, hh, vv]
tol = [kk, dd, yy, ww, tt, jj, uu, xx, hh, vv]
# 绿色，非绿色，总的评论的字符串
green_total = " ".join(green_tol)
gray_total = ' '.join(gray_tol)
total_comments = " ".join(tol)


def save(object, name):
    """
    保存上述字符串
    """
    filepath = 'F://' + name + ".txt"
    with open(filepath, "w", encoding="utf_8_sig") as f:
        f.write(object)


save(kk, "kk")
save(dd, "dd")
save(yy, "yy")
save(ww, "ww")
save(tt, "tt")
save(jj, "jj")
save(uu, "uu")
save(xx, "xx")
save(hh, "hh")
save(vv, "vv")
save(total_comments, "total")
save(green_total, "green")
save(gray_total, "gray")


# 使用两种方法提取标签


def get_tags(object):
    #     tags = jieba.analyse.extract_tags(object)
    tags = jieba.analyse.textrank(object)
    print(tags)
    return tags


kang_tags = get_tags(kk)
dun_tag = get_tags(dd)
yun_tag = get_tags(yy)
wan_tag = get_tags(ww)
tian_tag = get_tags(tt)
jing_tag = get_tags(jj)
you_tag = get_tags(uu)
xiang_tag = get_tags(xx)
hua_tag = get_tags(hh)
wei_tag = get_tags(vv)
t_tag = get_tags(total_comments)

# 绘制词云
f = open("F://positive_cut.txt", "r", encoding="utf_8_sig")
text = f.read()
f.close()
backgroud_Image = plt.imread('D://1.jpg')
wc = WordCloud(background_color='black',  # 设置背景颜色
               mask=backgroud_Image,  # 设置背景图片
               max_words=600,  # 设置最大现实的字数
               #                 stopwords = STOPWORDS,        # 设置停用词
               font_path=r'C:/Windows/Fonts/simkai.ttf',  # 设置字体格式，如不设置显示不了中文
               max_font_size=300,  # 设置字体最大值
               random_state=30,  # 设置有多少种随机生成状态，即有多少种配色方案
               )
wc.generate(text)
image_colors = ImageColorGenerator(backgroud_Image)
wc.recolor(color_func=image_colors)
plt.imshow(wc)
plt.axis('off')
plt.show()

# 绿色非绿色，总评论以，和。切割
li = []
for i in green:
    for j in i:
        sentences = [factor for factor in j.split('。')]
        for k in sentences:
            ss = [x for x in k.split('，')]
            li.extend(ss)


# 从标签中选择的关键词提取出相关评论
def get_comments_from_tags(ciyu, text):
    b = ""
    filepath = "D://" + ciyu + ".txt"
    for j in text:
        words = jieba.lcut(j)
        if ciyu in words:
            words.remove(ciyu)
            words = " ".join(words)
            words = "\n" + words
            with open(filepath, "a", encoding="utf_8_sig") as f:
                f.write(words)
            b += words
    return b


room = get_comments_from_tags("房间", li)
sevice = get_comments_from_tags("服务", li)
breakfast = get_comments_from_tags("早餐", li)
ruzhu = get_comments_from_tags("入住", li)
location = get_comments_from_tags("位置", li)
qiantai = get_comments_from_tags("前台", li)
enviroment = get_comments_from_tags("环境", li)
# sheshi=get_comments_from_tags("设施",li)
xingjiabi = get_comments_from_tags("性价比", li)

# 绘制房间早餐等的词云
f = open("F://gray//环境.txt", "r", encoding="utf_8_sig")
text = f.read()
f.close()
backgroud_Image = plt.imread('D://1.jpg')
wc = WordCloud(background_color='black',  # 设置背景颜色
               mask=backgroud_Image,  # 设置背景图片
               max_words=600,  # 设置最大现实的字数
               stopwords=stopwords,  # 设置停用词
               font_path=r'C:/Windows/Fonts/simkai.ttf',  # 设置字体格式，如不设置显示不了中文
               max_font_size=300,  # 设置字体最大值
               random_state=30,  # 设置有多少种随机生成状态，即有多少种配色方案
               )
wc.generate(text)
image_colors = ImageColorGenerator(backgroud_Image)
wc.recolor(color_func=image_colors)
plt.imshow(wc)
plt.axis('off')
plt.show()
