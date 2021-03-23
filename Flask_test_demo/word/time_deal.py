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
        print(times)
        global yestoday
        if yestoday not in save_time:
            save_time[yestoday]=1
        else:
            save_time[yestoday]+=1

def change():
    open('')