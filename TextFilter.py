# coding: utf-8
__author__ = 'LiNing'

import re
import nltk
import jieba
import jieba.analyse
import pymongo
import datetime


def MakeStopWordsList(stopwords_file):
    fp = open(stopwords_file, 'r') # stopwords_file最后有一个空行，可以添加或删除单词
    stopwords = []
    for line in fp.readlines():
        stopword = line.strip().decode("utf-8") # 由utf-8编码转换为unicode编码
        if len(stopword)>0:
            stopwords.append(stopword)
    fp.close()
    # 去重
    stopwords_list = sorted(list(set(stopwords)))
    return stopwords_list

def TextSeg(text, lag):
    if lag == "eng": # 英文情况
        word_list = nltk.word_tokenize(text)
    elif lag == "chs": # 中文情况
        #-------------------------------------------------------------------------------
        # jieba.enable_parallel(4) # 开启并行分词模式，参数为并行进程数，不支持windows
        word_cut = jieba.cut(text, cut_all=False) # 精确模式，返回的结构是一个可迭代的genertor
        word_list = list(word_cut) # genertor转化为list，每个词unicode格式
        # jieba.disable_parallel() # 关闭并行分词模式
        #-------------------------------------------------------------------------------
        # # jieba关键词提取
        # tags = jieba.analyse.extract_tags(text, topK=10)
        # # tags = jieba.analyse.textrank(text, topK=10)
        # print tags
        #-------------------------------------------------------------------------------
    return word_list

class MongoDBIO:
    # 申明相关的属性
    def __init__(self, host, port, name, password, database, collection):
        self.host = host
        self.port = port
        self.name = name
        self.password = password
        self.database = database
        self.collection = collection

    # 连接数据库，db和posts为数据库和集合的游标
    def Connection(self):
        # ##'''1.Connection'''
        # # connection = pymongo.Connection() # 连接本地数据库
        # connection = pymongo.Connection(host=self.host, port=self.port)
        # # db = connection.datas
        # db = connection[self.database]
        # if self.name or self.password:
        #     db.authenticate(name=self.name, password=self.password) # 验证用户名密码
        # print "Database:", db.name
        ##'''2.MongoClient'''
        ## mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]
        uri = "mongodb://%s:%s@%s:%d/%s" % (self.name, self.password, self.host, self.port, self.database)
        print uri
        client = pymongo.MongoClient(uri)
        db = client.get_default_database()

        # posts = db.cn_live_news
        posts = db[self.collection]
        print "Collection:", posts.name
        print posts.count()
        return posts

def DataFliter(host, port, name, password, database, collection, Limit_Number, lag, stopwords_set, content_column, time_column):
    print "......TextFilter System by LiNing......"
    print "filter_status equals 1 means OK, otherwise 0"
    posts = MongoDBIO(host, port, name, password, database, collection).Connection()

    #-------------------------------------------------------------------------------
    # 以下几行根据实际情况修改

    #### 查询操作
    id_dict = {"0":[], "1":[]} # 1-表示通过，0-表示不通过

    starttime = datetime.datetime(2015, 1, 1)
    endtime = datetime.datetime.now()
    for post in posts.find({
        time_column:{"$gte":starttime, "$lte":endtime},
        content_column:{"$exists":1},
        "filter_status":{"$exists":0}
    },).sort(time_column, pymongo.DESCENDING).limit(Limit_Number):
        # print post
        if post[content_column] is not None:
            # print post["content"]
            textseg_list = TextSeg(post[content_column], lag)
            testseg_set = set(textseg_list)
            if stopwords_set & testseg_set:
                id_dict["0"].append(post["_id"])
            else:
                id_dict["1"].append(post["_id"])
        else:
            print '{"_id":ObjectId("%s")} None' % post["_id"]

    #### 更新操作
    for id in id_dict["0"]:
        posts.update({"_id":id}, {"$set":{"filter_status":0}})
        print '{"_id":ObjectId("%s")} 0' % id
    for id in id_dict["1"]:
        posts.update({"_id":id}, {"$set":{"filter_status":1}})
        print '{"_id":ObjectId("%s")} 1' % id
    #-------------------------------------------------------------------------------


if __name__ == '__main__':

#-------------------------------------------------------------------------------
    try:
        with open("./Config/config", "r") as fp:
            lines = fp.readlines() # list
    except Exception as e:
        print e
        exit()
    for line in lines:
        if re.match(r'^lag', line):
            lag = str(re.search(r'"(.*?)"', line).group(1)) # 从任意位置只找出第一个成功的匹配
        elif re.match(r'^Limit_Number', line):
            Limit_Number = int(re.search(r'.*?\s*=\s*(\d+?)\s', line).group(1))
        elif re.match(r'^host', line):
            host = str(re.search(r'"(.*?)"', line).group(1))
        elif re.match(r'^port', line):
            port = int(re.search(r'.*?\s*=\s*(\d+?)\s', line).group(1))
        elif re.match(r'^name', line):
            name = str(re.search(r'"(.*?)"', line).group(1))
        elif re.match(r'^password', line):
            password = str(re.search(r'"(.*?)"', line).group(1))
        elif re.match(r'^database', line):
            database = str(re.search(r'"(.*?)"', line).group(1))
        elif re.match(r'^collection', line):
            collection = str(re.search(r'"(.*?)"', line).group(1))
        elif re.match(r'^content_column', line):
            content_column = str(re.search(r'"(.*?)"', line).group(1))
        elif re.match(r'^time_column', line):
            time_column = str(re.search(r'"(.*?)"', line).group(1))

    stopwords_file = "./Config/stopwords_"+lag
    stopwords_list = MakeStopWordsList(stopwords_file)
    stopwords_set = set(stopwords_list)

#-------------------------------------------------------------------------------

    DataFliter(host, port, name, password, database, collection, Limit_Number, lag, stopwords_set, content_column, time_column)

