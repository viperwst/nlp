import requests
import urllib.parse
from spider import ip
import json
import os
import csv


def get_url(key_word,page,start_time):
    change_word = urllib.parse.quote('=60&q=' + key_word + '&t=0')
    for i in range(1,int(page)+1):
        url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type' \
              + change_word + '&page_type=searchall' + str(i)
        get_content(url,0,start_time)
    return use_deal_time()

def get_content(url,num,start_time):
    ip_ = ip.random_ip()
    headers = {
        'cookie': '_T_WM=65441121645; WEIBOCN_WM=3349; H5_wentry=H5; backURL=https%3A%2F%2Fm.weibo.cn%2F; SCF=AmksqbcT9SbyenOBUv4x3Ope-hQdHVFccE6wStttA-lV9amgbq4gI5lmLbMB387UMLB1xsvjr2vkERg5LO45PXE.; SUB=_2A25ym7HWDeRhGeRK7lEX8SrOzj2IHXVuZ9-erDV6PUJbktANLW3mkW1NU1JLIZSyXBytNWj9jvVOp6z92YS8Q21d; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W56JwhGXo.8QUZEaD.eAFMw5NHD95QESh-0So2Xeo-pWs4DqcjeHJL79Pz_MspywgHE; SUHB=0rr6QoySdcTIFO; SSOLoginState=1604305286; WEIBOCN_FROM=1110005030; MLOGIN=1; XSRF-TOKEN=140648; M_WEIBOCN_PARAMS=oid%3D4565826198316714%26luicode%3D20000061%26lfid%3D4565826198316714%26uicode%3D20000061%26fid%3D4565826198316714',
        'X-Requested-With': 'XMLHttpRequest',
        'X-XSRF-TOKEN': 'f2dec6',
        'Referer': 'https://m.weibo.cn/detail/4565826198316714',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36'
    }
    regt = requests.get(url,headers=headers,proxies=ip_,timeout=3)
    if regt.status_code == 200:
        print('连接成功')
        if num == 0:
            get_id(regt.text)
        elif num == 1:
            get_comment(regt.text,start_time)
    else:
        print('连接失败')

def get_id(text):
    id_list = []
    reg = json.loads(text)
    len_ = len(reg['data']['cards'])
    for i in range(len_):
        id = reg['data']['cards'][i]['mblog']['id']
        id_list.append(id)
    get_url_id(id_list)

def get_url_id(list):
    page = 1
    for i in list:
        for k in range(page):
            try:
                url = 'https://m.weibo.cn/api/comments/show?id=' + i + '&page=' + str(k)
                get_content(url,1)
            except:
                print('超过')
        continue

#时间处理
import time
global save_time
save_time=dict()
global today
today=time.localtime(time.time())
today=str(today[1])+'-'+str(today[2])
global yestoday
yestoday=str(today[:2])+'-'+str(int(today[-2:])-1)
save_time[today]=0
def deal_time(times):
    print(times)
    if '小时前' in times:
        global save_time
        save_time[today]+=1
    elif '分钟前' in times:
        save_time[today]+=1
    elif '-' in times:
        if times not in save_time:
            save_time[times]=1
        else:
            save_time[times]+=1
    elif '昨天' in times:
        # print(times)
        global yestoday
        if yestoday not in save_time:
            save_time[yestoday]=1
        else:
            save_time[yestoday]+=1

#保存文本
def get_comment(text,start_time):
    reg = json.loads(text)
    len_ = len(reg['data']['data'])
    for i in range(len_):
        text = reg['data']['data'][i]['text']
        times = reg['data']['data'][i]['created_at']
        print(text)
        # print('时间',times)
        deal_time(times)
        if '回复' in text and '@' in text:
            text = text.split('</a>:')[1].split('<span')[0]
            save_comment(text,start_time)

def save_comment(text,start_time):
    # print('yes')
    csv_path = os.getcwd() + '\\comment_deal\\comments\\{}.csv'.format(start_time)
    csvfile = open(csv_path, 'a+', encoding='utf-8', newline='')
    print('开始写文件')
    writer = csv.writer(csvfile)
    writer.writerow([text])
    csvfile.flush()
    csvfile.close()


def use_deal_time():
    return save_time

if __name__ == '__main__':
    key_word = input('请输入关键词:')
    page = input('请输入爬取的页数:')
    get_url(key_word,page)
