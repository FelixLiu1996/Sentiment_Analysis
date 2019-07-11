import numpy as np
import pandas as pd
import jieba
from gensim.models import Word2Vec, KeyedVectors, word2vec

file_path = "D:\PythonCodes\Python_Course_Project/"

with open(file_path + 'positive_cut.txt', encoding='utf-8') as f:
    sentences = f.read()

with open(file_path + 'negative_cut.txt', encoding='utf-8') as f:
    sentences += f.read()

# sentences = word2vec.Text8Corpus(file_path + 'all_cut.txt')

# 构建Word2vec模型
model = word2vec.Word2Vec(sentences, size=200, min_count=1)
model.wv.save_word2vec_format(file_path + 'word_to_vec.txt', binary=False)
model.wv.save(file_path + 'word_to_vec.model')
