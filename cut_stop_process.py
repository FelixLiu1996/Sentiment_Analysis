import numpy as np
import pandas as pd
import jieba
import jieba.analyse
import re
import codecs
import string


def clean_data(text):
    """去掉标点符号以及中文 """
    pattern = re.compile("[\u4e00-\u9fa5]|[\（\）\《\》\——\；\，\。\“\”\<\>\！]")  # 只匹配标点符号和中文
    res = pattern.findall(text)
    res = ''.join(res)
    return res


def stopwordlist(filepath):
    """
    加载停用词列表
    并且将一些对于本研究相关的无用的词添加到停用词表中

    """
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    stopwords.extend(['大连', '酒店', '宾馆', '康莱德', '希尔德', '友谊', '希尔顿', '良运', '香格里拉', '维多利亚', '船舶丽湾'])
    return stopwords


def seg_sentence(sentence):
    """
    进行去停用词
    :param sentence: 需要去停用词的句子
    :return: 返回去除的结果
    """
    sentence_seged = jieba.cut(sentence.strip())
    stopwords = stopwordlist(file_path + '哈工大停用词表.txt')  # 加载停用词的路径
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr


# 文本分割
def sent2word(line):
    """
    对文本进行分词操作

    """

    segList = jieba.cut(line, cut_all=False)
    segSentence = ''
    for word in segList:
        if word != '\t':
            segSentence += word + " "
    return segSentence.strip()


file_path = "D:\PythonCodes\Python_Course_Project/"

# 将正样本进行 去英文等 分词 去停用词 等操作
with open(file_path + "positive.txt", encoding='utf-8') as f:
    positive = f.readline()
    target = open(file_path + 'positive_cut.txt', encoding='utf-8', mode='w')
    while positive:
        positive = clean_data(positive)
        positive = sent2word(positive)
        positive = seg_sentence(positive)
        target.writelines(positive + '\n')
        positive = f.readline()

    target.close()

with open(file_path + 'negative.txt', encoding='utf-8') as f:
    negative = f.readline()
    target = open(file_path + 'negative_cut.txt', encoding='utf-8', mode='w')
    while negative:
        negative = clean_data(negative)
        negative = sent2word(negative)
        negative = seg_sentence(negative)
        target.writelines(negative + '\n')
        negative = f.readline()

    target.close()

# positive = pd.read_table(file_path + "positive.txt")
# negative = pd.read_table(file_path + "negative.txt", header=None, index_col=False)
# print(positive)
# print(negative[0])
# print(type(positive))
#
# # with open(file_path + "positive.txt", encoding='utf_8') as f:
# #     positive = f.readline()
# #     # print(positive)
# #     print(positive)
# #     positive = f.readline()
# #     print(positive)
#
# def prepareData(sourceFile, targetFile):
#     f = codecs.open(sourceFile, 'r', encoding='utf-8')
#     target = codecs.open(targetFile, 'w', encoding='utf-8')
#     print('open source file: ' + sourceFile)
#     print('open target file: ' + targetFile)
#
#     lineNum = 1
#     line = f.readline()
#     while line:
#         print('---processing ', lineNum, ' article---')
#         # line = clearTxt(line)
#         # line = clear_data(line)
#         seg_line = sent2word(line)
#         target.writelines(seg_line + '\n')
#         lineNum = lineNum + 1
#         line = f.readline()
#     print('well done.')
#     f.close()
#     target.close()
#
#
# # 清洗文本
# # def clearTxt(line):
# #     if line != '':
# #         line = line.strip()
# #         intab = ""
# #         outtab = ""
# #         trantab = str.maketrans(intab, outtab)
# #         pun_num = string.punctuation + string.digits
# #         line = line.encode('utf-8')
# #         line = line.translate(trantab, pun_num)
# #
# #         line = line.decode("utf8")
# #         # 去除文本中的英文和数字
# #         # line = re.sub("[a-zA-Z0-9]", "", line)
# #         # # 去除文本中的中文符号和英文符号
# #         # line = re.sub("[\s+\.\!\/_,$%^*(+\"\'；：“”．]+|[+——！，。？?、~@#￥%……&*（）]+".decode("utf8"), "", line)
# #         line = clean_data(line)
# #     return line
#
#
# # 文本切割
# def sent2word(line):
#     segList = jieba.cut(line, cut_all=False)
#     segSentence = ''
#     for word in segList:
#         if word != '\t':
#             segSentence += word + " "
#     return segSentence.strip()
#
#
# if __name__ == '__main__':
#     sourceFile = file_path + 'negative.txt'
#     targetFile = file_path + 'negative_cut.txt'
#     sourceFile = clean_data(sourceFile)
#     prepareData(sourceFile, targetFile)
#
#     sourceFile = file_path + 'positive.txt'
#     targetFile = file_path + 'positive_cut.txt'
#     prepareData(sourceFile, targetFile)
#     # file_path = "D:\PythonCodes\Python_Course_Project/"
#     # with open(file_path + "positive.txt", encoding="utf_8") as f:
#     #     positive = f.read()
#     #
#     # seg =jieba.lcut(positive, cut_all=False)
#     # print('/'.join(seg))
