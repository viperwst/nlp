import time

from flask import Flask, request, render_template, redirect, url_for
from spider import 爬虫
import os
from model import 模型使用 as u_model
# from spider import tieba
from word import 词云 as  word_analyse

import pandas as pd

app = Flask(__name__)

global time_dict
time_dict=dict()

@app.route('/',methods=['GET','POST'])
def index():
    print('post')


    return render_template('home.html')

@app.route('/home',methods=['GET','POST'])
def home():
    # print('主页')
    if request.method == 'POST':
        key_word = request.form.get('key_word')
        page = request.form.get('page')
        global time_dict
        #爬虫判断
        spi=request.form.get('spi')
        print(spi)
        start_time = str(int(round(time.time() * 1000)))

        if spi=='wb':
            time_dict=爬虫.get_url(key_word, page,start_time)
        elif spi=='zh':
            print('启动zh')
            # time_dict = tieba.get_url(key_word, page)
        # 判断需要的文件是否存在，存在则运行下一个函数
        if os.path.exists('comment_deal/comments/{}.csv'.format(start_time)):
            u_model.use_model(start_time) # 传入一个名字
            return redirect(url_for('table1',start_time=start_time))
        # 获得函数运行的结果

        else:
            print('sorry')
            return '失败'


def test(pd_path):
    # pd_path=os.getcwd()+'\\comment_deal\\commcomments_classify\\微博评论.csv'
    # if os.path.exists(pd_path):
        a = pd.read_csv(pd_path, engine='python', encoding='utf-8')
        b = a['分类'].value_counts()
        print(b['负向'])
        print(b['正向'])
        count = dict()
        count['正向'] = str(b['正向'])
        count['负向'] = str(b['负向'])
        return count
    # else:
    #     print(pd_path)
    #     print('错误')

global data
data=dict()
import json

#高频词统计
@app.route('/table1/?<string:start_time>',methods=['GET','POST'])
def table1(start_time):
    # # 调用词云分析模块

    word_path=os.getcwd()+'\\comment_deal\\comments_classify\\{}.csv'.format(start_time)
    if os.path.exists(word_path):
        top10,pd_count=word_analyse.use(start_time)
        global time_dict
        count=test(pd_count)
        global data
        data={
            'comment': top10,
            'time':time_dict,
            'count': count
        }
        data=json.dumps(data)
        print(data)
        return render_template('微博图1.html',data=data)
    else:return '路径找不到'

#折线图
@app.route('/table2',methods=['GET','POST'])
def table2():
    return render_template('微博图2.html',data=data)


#饼图
@app.route('/table3',methods=['GET','POST'])
def table3():
    # # # 调用词云分析模块
    # top10,pd_count=word_analyse.use()
    # global time_dict
    # count=test(pd_count)
    # data={
    #     'comment': top10,
    #     'time':time_dict,
    #     'count': count
    # }
    # data=json.dumps(data)
    # print(data)
    return render_template('微博图3.html',data=data)

#词云

if __name__ == '__main__':
    app.run()

'''
1、导入Flask框架
2、创建Flask程序实例
3、定义路由及视图函数
4、运行程序
'''
