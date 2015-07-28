<h1>Ubuntu Linux下环境搭建：</h1>
<pre><code>
sudo apt-get install python-pip
pip install nltk
pip install jieba
pip install pymongo
</code></pre>

<h1>敏感词过滤系统by宁哥：</h1>
<p><strong>Config下config文件：</strong></p>
<p>可以进行服务器配置，针对数据库中制订collection的不同字段column，</p>
<p>可以选择语言(中文，英文)，</p>
<p>可以设置要过滤的文章数目，时间默认从最近前推</p>
<p>添加邮件通知系统，SendMailFlag = &quot;Yes&quot; # &quot;No&quot; 一行可以修改是否接收邮件通知</p>
<p>结果：字段filter_status为1表示通过过滤，为0表示不通过过滤</p>
<p><strong>stopwords_chs和stopwords_eng为过滤词黑名单</strong></p>
<p>可以随时添加要过滤的单词，一行一个</p>
<p>如果添加的过滤词无法正确被jieba分词，则同样方法将该需要过滤的词及词频加入到dict文件中，一行一个</p>
<p>如stopwords_chs，加入了“阿尼玛”换行， 在dict中加入“阿尼玛 3”，3表示词频，词频越大分词越准确</p>
