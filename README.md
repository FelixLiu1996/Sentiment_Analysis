# Sentiment_Analysis
python课的结课作业

## 使用selenium与xpath动态爬取携程网站大连十家酒店（5家绿色，5家非绿色）的评论、评分以及其他一些相关信息

## 数据处理
将评论数小于4个字的评论删除，将重复的评论删除去重
对评论进行分词，去停用词（使用哈工大去停用词加本文特有的一些词汇，如酒店等等）

## 绘制词云图
通过提取特征，通过这些特征选择评论进行词云图的绘制
绘制绿色酒店与非绿色酒店的词云图

## 建模
经过分词、去停用词等等操作的数据，构建LSTM模型
