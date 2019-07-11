import numpy as np
import pandas as pd
import gensim
from gensim.models import KeyedVectors, Word2Vec, word2vec
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import keras
from keras.models import Sequential
from keras.layers import Activation, Dense, LSTM, Embedding
from keras.optimizers import SGD, Adam
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_curve, auc
from imblearn.over_sampling import SMOTE
from keras.callbacks import TensorBoard
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import BernoulliNB, MultinomialNB

file_path = "D:\PythonCodes\Python_Course_Project/"

# 导入知乎问答语料库作为之后模型训练的语料库
model = KeyedVectors.load_word2vec_format(file_path + 'sgns.zhihu.bigram')

# 将分词之后的每条评论的分词转换成词索引的列表training_tokens
training_tokens = []

with open(file_path + "all_cut.txt", encoding='utf-8') as f:
    text = f.readline()
    while text:
        text = text.split()
        for i, word in enumerate(text):
            # 将词转换为索引，如果词不在词向量中，则设为0
            try:
                text[i] = model.vocab[word].index
            except KeyError:
                text[i] = 0
        training_tokens.append(text)
        text = f.readline()

vocab_list = [(k, model.wv[k]) for k, v in model.wv.vocab.items()]

# 存储所有word2vec中所有向量的数组
embeddings_matrix = np.zeros((len(model.wv.vocab.items()), model.vector_size))

#
for i in range(len(vocab_list)):
    word = vocab_list[i][0]
    embeddings_matrix[i] = vocab_list[i][1]

# 训练的样本的label， 本文中正样本数为12798，设为1   负样本数1172  设为0
training_label = np.concatenate((np.ones(12798), np.zeros(1172)))

# num_tokens = [len(tokens) for tokens in training_tokens]
# print(np.sum(num_tokens < 50 / len(num_tokens)))
# 选择一个合适的数， 对training_tokens进行一个填充或者截断处理
pad_training_tokens = pad_sequences(training_tokens, maxlen=50)
x_train, x_test, y_train, y_test = train_test_split(pad_training_tokens, training_label, test_size=0.2,
                                                    random_state=123)

# 因为正负样本十分不均衡，比例几乎达到13：1，所以使用SMOTE算法解决样本不均衡问题
pad_training_tokens_2, training_label_2 = SMOTE().fit_sample(pad_training_tokens, training_label)
x_train_2, x_test_2, y_train_2, y_test_2 = train_test_split(pad_training_tokens_2, training_label_2, test_size=0.2,
                                                            random_state=123)
# print(x_train_2)
# print(x_test_2.shape)

# 进行建模

# 尝试进行可视化

# 使用Tensorboard进行可视化
tbCallBack = TensorBoard(log_dir='D:/PythonCodes/Python_Course_Project/lstm1_logs',  # log 目录
                         histogram_freq=0,  # 按照何等频率（epoch）来计算直方图，0为不计算
                         write_graph=True,  # 是否存储网络结构图
                         write_grads=True,  # 是否可视化梯度直方图
                         write_images=True,  # 是否可视化参数
                         embeddings_freq=0,
                         embeddings_layer_names=None,
                         embeddings_metadata=None)

# 进行模型的构建
lstm2_model = Sequential()
# 添加一层嵌入层, 将之前的索引的列表转换成固定尺寸的向量
lstm2_model.add(Embedding(embeddings_matrix.shape[0],
                          embeddings_matrix.shape[1],
                          weights=[embeddings_matrix],
                          input_length=50,
                          trainable=False))
# 加入LSTM层
lstm2_model.add(LSTM(units=10, return_sequences=True))
lstm2_model.add(LSTM(units=20, kernel_initializer='uniform', activation='relu', return_sequences=True))
lstm2_model.add(LSTM(units=10, return_sequences=False))

# 输出层
lstm2_model.add(Dense(units=1, kernel_initializer='uniform', activation='sigmoid'))

# 模型编译以及模型训练
lstm2_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
lstm2_model.fit(x_train_2, y_train_2, validation_split=0.2, epochs=20, batch_size=20, verbose=1, callbacks=[tbCallBack])

# 模型效果的评估，指标使用AUC值
pred = lstm2_model.predict(x_test_2)
print("AUC: %4f" % (metrics.roc_auc_score(y_test_2, pred)))

# 绘制ROC曲线
fpr, tpr, thresholds = roc_curve(y_test_2, pred)

auc_lstm = auc(fpr, tpr)
plt.plot([0, 1], [0, 1], 'k--')
plt.plot(fpr, tpr, label="AUC:0.9814")
plt.xlabel('False positive rate')
plt.ylabel('True positive rate')
plt.plot()
plt.legend(loc='best')
plt.show()

# 构建机器学习模型

# Naive Bayes
classifier = BernoulliNB()
# classifier = MultinomialNB()
classifier.fit(x_train_2, y_train_2)
accu = classifier.score(x_test_2, y_test_2)
print(accu)

# Logistic Regression
lr = LogisticRegression()
lr.fit(x_train_2, y_train_2)
lr.predict_proba(x_test_2)
print(lr.score(x_test_2, y_test_2))
auc = cross_val_score(lr, x_train_2, y_train_2, cv=10, scoring='roc_auc').mean()
print(auc)

# SVM
svm = svm.SVC()
svm.fit(x_train_2, y_train_2)
# svm.predict_proba(x_test_2)
print(svm.score(x_test_2, y_test_2))
auc = cross_val_score(svm, x_train_2, y_train_2, cv=10, scoring='roc_auc').mean()
print("AUC: %4f" % (auc))
