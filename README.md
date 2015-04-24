Ubuntu Linux下环境搭建：
sudo apt-get install python-pip
pip install nltk
pip install jieba
pip install pymongo


敏感词过滤系统by宁哥

Config下config文件：
可以进行服务器配置，针对数据库中制订collection的不同字段column，
可以选择语言(中文，英文)，
可以设置要过滤的文章数目，时间默认从最近前推
结果：字段filter_status为1表示通过过滤，为0表示不通过过滤

stopwords_chs和stopwords_eng为过滤词黑名单
可以随时添加要过滤的单词，一行一个

