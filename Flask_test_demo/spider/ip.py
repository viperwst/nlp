import random
import os
def random_ip():
    ip_path=os.getcwd()+'\\spider\\ip.text'
    # print('iptext:',ip_path)
    with open(ip_path,'r') as f:
        data = f.readlines()
        f.close()

    reg = []
    for i in data:
        k = eval(i)
        reg.append(k)
    ip = random.choice(reg)
    return ip

if __name__ == '__main__':
    random_ip()