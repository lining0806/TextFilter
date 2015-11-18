# 敏感词过滤系统

### **更多详见[TextMining](https://github.com/lining0806/TextMining)**

***

**Ubuntu Linux下环境搭建：**
 
    sudo apt-get install python-pip  
    pip install nltk  
    pip install jieba  
    pip install pymongo  

**Config下config文件：**  
* 可以进行服务器配置，针对数据库中制订collection的不同字段column，  
* 可以选择语言(中文，英文)，  
* 可以设置要过滤的文章数目，时间默认从最近前推  
* 添加邮件通知系统，SendMailFlag = "Yes" # "No" 一行可以修改是否接收邮件通知  
* 结果：字段filter_status为1表示通过过滤，为0表示不通过过滤  

**stopwords_chs和stopwords_eng为过滤词黑名单**    
* 可以随时添加要过滤的单词，一行一个  
* 如果添加的过滤词无法正确被jieba分词，则同样方法将该需要过滤的词及词频加入到主词典dict文件中或者用户词典user_dict，一行一个（词频也可省略）  
* 如stopwords_chs，加入了“阿尼玛”换行， 在dict中加入“阿尼玛 3”，3表示词频，词频越大分词越准确