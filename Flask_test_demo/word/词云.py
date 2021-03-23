import pandas as pd
# import pymysql
from sqlalchemy import create_engine
import re
import jieba
import jieba.analyse
import os

baidu = os.getcwd() + '\\word\\baidu_stopwords.txt'
stop = os.getcwd() + '\\word\\stop.txt'
cn = os.getcwd() + '\\word\\cn_stopwords.txt'
stopwords1 = [line.rstrip() for line in open(baidu, 'r', encoding='utf-8')]
stopwords2 = [line.rstrip() for line in open(stop, 'r', encoding='utf-8')]
stopwords3 = [line.rstrip() for line in open(cn, 'r', encoding='utf-8')]

stopwords = stopwords1 + stopwords2 + stopwords3

meaninful_words = []

# 1.从数据库导入微博数据并查看
def check(start_time):
    csv_os = os.getcwd() + '\\comment_deal\\comments_classify'
    mblog_frame = pd.read_csv(csv_os + '\\{}.csv'.format(start_time), index_col=None)
    # print(mblog_frame)
    return mblog_frame


# 2.清除text中的非微博正文字符并抽取关键词
# 自定义函数
def clean_text(raw):
    """
    清除text中的非微博正文字符
    返回值类型为元组
    """
    if raw['评论']:
        text = re.sub('<[^<]*>', '', raw['评论'])  # 清除多余的html语句
        text = re.sub('[#\n]*', '', text)  # 清除换行符与#符号
        text = re.sub('(http://.*)$', '', text)  # 清除文末的网址
        text = raw['评论']
        return text
    else:
        return None


def get_chinese_text(raw):
    """
    清除text中的非中文字符
    只能提取中文字符，微博中的数字以及英文均会丢失
    """
    if raw['评论']:
        res_text = ''.join(re.findall(r"[\u4e00-\u9fff]{2,}", raw['评论']))
        if res_text:
            return res_text
    else:
        return None



def get_keywords(raw):
    """
    使用jieba从中文text抽取关键词
    默认抽取20个关键词
    longtext 提取40个关键词
    """
    # if raw['chinese_text']:
    #     if raw['isLongText'] == 1:
    #         # 当text为长文本时，提取50个关键词
    #         keywords = jieba.analyse.extract_tags(raw['chinese_text'], topK=50)
    #     else:
            # 当text为非长文本时，默认提取20个关键词
    if raw['评论']:
        # print(raw['cleaned_comment'])
        keywords = jieba.analyse.extract_tags(raw['评论'])
        for word in keywords:
            if word in stopwords:
                keywords.remove(word)
            else:
                meaninful_words.append(word)
        # print(keywords)
        # raw['mid'],
        return (keywords)
    else:
        return None


def clean_created_date(raw):
    created_date = raw['created_at']
    if created_date.endswith('前'):
        created_date = '11-03'
    elif created_date.startswith('昨天'):
        created_date = '11-02'
    return created_date


# 获取清理后的created_date
# mblog_frame['created_at'] = mblog_frame.apply(clean_created_date, axis=1)
# 获取清理后的text
def after(mblog_frame):
    print('测试：',mblog_frame)
    mblog_frame['评论'] = mblog_frame.apply(get_chinese_text, axis=1)

# 以传入字典items()的形式生成DataFrame，指定列名
    res_mblog = pd.DataFrame(mblog_frame, columns=['评论','分类'])
# 写入csv文件便于查看数据清洗结果
# res_mblog.to_csv('jiazhangqun3.csv', encoding='utf_8_sig', index=False)
# 获取关键字并转换为分散存储的DataFrame
    mid_with_keyword = list(mblog_frame.apply(get_keywords, axis=1))
    #print(mid_with_keyword)
# 这里要把keywords列表存储到数据库，因此需要将keywords列表分开，并与mid对应
    keywords_list = [w for raw in mid_with_keyword for w in raw]

    mid_with_keyword = pd.DataFrame(keywords_list, columns=['keyword'])
# 写入csv文件便于查看结果
    mid_with_keyword.to_csv('keyword1.csv', encoding='utf_8_sig', index=False)
# 从数据库读取微博数据
    keyword_frame = pd.read_csv('keyword1.csv', index_col=False)
# 取出全部的关键词，并生成一个列表
    all_keyword = list(keyword_frame.keyword)

# 使用collections模块中的Counter统计每个关键词出现的次数，Counter返回一个字典，keyword：count
    from collections import Counter

    word_freq_frame = pd.DataFrame(Counter(all_keyword).items())
    word_freq_frame.columns = ['word', 'count']
    top100_freq_word = word_freq_frame.sort_values('count', ascending=0).head(100)
    top3_freq_word = word_freq_frame.sort_values('count', ascending=0).head(3)
    top100_freq_word_dict = dict(list(top100_freq_word.apply(lambda w: (w['word'], w['count']), axis=1)))
    top3= dict(list(top3_freq_word.apply(lambda w: (w['word'], w['count']), axis=1)))
# #计算词频，一行解决
    print('词频:',top100_freq_word)
    print('字典:',top3)
    from wordcloud import WordCloud, STOPWORDS
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来显示负号
    plt.rcParams['figure.dpi'] = 100  # 分辨率
    wc = WordCloud(background_color="white", max_words=2000, font_path='simhei.ttf')
    wc.generate_from_frequencies(top100_freq_word_dict)
    # 存到指定路径下
    png_os = os.getcwd() + '\\static\\wordcoud.png'
    wc.to_file(png_os)
    plt.imshow(wc)
    plt.axis('off')
    plt.show()
    return top3

def use(start_time):
    word_path=os.getcwd()+'\\comment_deal\\comments_classify\\{}.csv'.format(start_time)
    if os.path.exists(word_path):
        top10=after(check(start_time))
        print(top10,word_path)
        return top10,word_path
    else:
       print('error')


