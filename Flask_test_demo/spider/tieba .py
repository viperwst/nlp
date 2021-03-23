import requests
from lxml import etree
import sys
import os
import urllib
import re,csv
global times
times=dict()

def get_url(key_word, page):
    # 1. 创建文件对象
    # csv_path = os.getcwd() + '\\comment_deal\\comments\\微博评论(单评论改进版1).csv'
    f = open('1.csv','w',encoding='utf-8')
    # 2. 基于文件对象构建 csv写入对象
    csv_writer = csv.writer(f)




    i = 1
    lst = []
    key = key_word
    key = urllib.parse.quote(key)

    # url = 'https://tieba.baidu.com/f/search/res?ie=utf-8&qw=%s'%key

    headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
        }
    while i <= int(page):
        url = 'https://tieba.baidu.com/f/search/res?isnew=1&kw=&qw=' + key + '&rn=10&un=&only_thread=0&sm=2&sd=&ed=&pn=' + str(
            i)
        # print(url)
        response = requests.get(url=url,headers=headers)
        # response.encoding='utf-8'
        page_text = response.text
        # print(page_text)
        html = re.findall('class="p_content">(.*?)</div',page_text)
        date = re.findall('class="p_green p_date">(.*?)</font>',page_text)
        for j in range(len(date)):
        # for content in html:
            content = html[j]
            content = content.replace('<em>','')
            content = content.replace('</em>', '')
            datetime = date[j]
            time=datetime[5:10]
            global times
            if time in times:
                times[time]+=1
            else:times[time]=1
            print(content,datetime)
            csv_writer.writerow([content])
        i = i+1
    print(times)
    times=sorted(times.items(),key=lambda x:(int(x[0][0:2]),int(x[0][3:5])))
    print(dict(times))
    return times

if __name__ == '__main__':
    key_word = input('请输入关键词:')
    page = input('请输入爬取的页数:')
    get_url(key_word,page)