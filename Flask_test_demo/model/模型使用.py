#模型预测
import jieba
import joblib
import pandas as pd
#用各个词向量直接平均的方式生成整句对应的词向量
import gensim
import csv
import os

def m_avgver(words,w2vmodel):
    return pd.DataFrame([w2vmodel.wv[w] for w in words if w in w2vmodel.wv]).agg('mean')

def predict(string,model):
    #导入词向量表
    w2=os.getcwd()+'\\词向量训练\\词向量表'
    w2vmodel = gensim.models.word2vec.Word2Vec.load(w2)
    words=jieba.cut(string)
    words_vecs=pd.DataFrame(m_avgver(words,w2vmodel)).T
    result=model.predict(words_vecs)
    # print(string)
    resultstr=''
    # print(result,end='')
    if int(result[0])==1:
        # print('正向')
        resultstr='正向'
    else:
        # print('负向')
        resultstr='负向'
    return resultstr

def use_model(start_time):
    #if os.path.exists('../微博评论(单评论改进版1).csv'):
        csv_path=os.getcwd()+'\\comment_deal\\comments\\{}.csv'.format(start_time)
        df=pd.read_csv(csv_path, engine='python', encoding='utf-8', header=None)

        #使用随机森林模型
        tree=os.getcwd()+'\\词向量训练\\随机森林模型'
        random_tree = joblib.load(tree)
        tree_classify=os.getcwd()+'\\comment_deal\\comments_classify\\{}.csv'.format(start_time)
        csvfile=open(tree_classify, 'w', encoding='utf-8', newline='')
        writer=csv.writer(csvfile)
        writer.writerow(('评论','分类'))
        for comment in range(1,len(df)):
            com=str((df[comment-1:comment].values)[0][0])
            result=predict(str(df.iloc[comment]),random_tree)
            # print([com,result])
            writer.writerow([com, result])
    #else:
        # print('very sorry')
        csvfile.flush()
        csvfile.close()
if __name__ == '__main__':
    use_model()