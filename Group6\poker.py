import random
import time
import paixing

'''
确认玩家数（2-10人）
发放底牌-每人两张
    random从剩余的牌库中取出
发新的公共牌并判断
    发放公共牌-一共三轮
        random从剩余的牌库中取出
    玩家轮流查看底牌
输出最终的牌型最大的玩家
'''

number = int(input('请输入玩家人数：'))
#number = 4
A=['♥','♠','♦','♣']
B=['3','4','5','6','7','8','9','10','J','Q','K','A','2']
poker=[]
pokers=[]
pokername=[]
n=1
for i in A:
    for j in B:
         pokers.append((n,(i+j)))
         n=n+1
print("开始洗牌....")
#print(pokers)
random.shuffle(pokers)


#定义洗牌
def xipai(x):
    for i in x:
        pokers.remove(i)
    return pokers

#定义发牌
def fapai(y):
    for i in y:
        print(i[1],',',end=" ")

#定义函数：每个人发两张底牌
def fadipai(number):
    time.sleep(3)
    global pokers
    for i in range(number):
        pokername.append(random.sample(pokers,2))
        pokers = xipai(pokername[i])
        print("\n开始给player{}发牌：".format(i+1))
        fapai(pokername[i])
        pokername[i].sort()

#定义函数：发公共牌
pai=[]
def fagongpai(x,t):
    global pokers
    global pai
    time.sleep(3)
    gongpai=random.sample(pokers,x)
    pokers = xipai(gongpai)
    print("\n开始发第{}轮公牌：".format(t))
    gongpai.sort()
    pai = gongpai
    '''
    for i in gongpai:
        pai.append(i)
    '''
    fapai(pai)
    return pai

#定义函数：玩家轮流查看底牌
def chakanpai(number):
    print('\n')
    '''
        for i in range(number):
        kan = int(input('\n请输入看牌玩家号：'))
        print("\nplayer{}的牌：".format(kan))
        for i in pai:
            pokername[kan - 1].append(i)
        fapai(pokername[kan-1])
        #print(pokername[kan-1])
        #return pokername[kan-1].sort()
    '''
    fenshu = []
    for i in range(number):
        #jibie = 0
        #type = ''
        for j in pai:
            pokername[i].append(j)
        print("player{}的牌：".format(i+1))
        fapai(pokername[i])
        jibie = paixing.zuiyou(pokername[i])
        type = paixing.panduan(pokername[i])
        print(paixing.panduan(pokername[i]))
        fenshu.append(jibie)
        print('权值：{:.8f}'.format(jibie))
    print('玩家{}牌最大'.format(fenshu.index(max(fenshu))+1))
    #print(pokername[i])


'''
def shunzi():
    for i in range(number):
        print('\n',max(pokername[i])[0])
        print('\n',max(pokername[i]))
        print(min(pokername[i])[0],'\n')
        print(min(pokername[i]),'\n')
'''

def main():
    fadipai(number)  # 发底牌
    # chakanpai(number)#玩家查看牌

    fagongpai(3, 1)  # 发第一轮公牌，3张
    chakanpai(number)  # 玩家查看牌

    fagongpai(1, 2)  # 发第二轮公牌，1张
    chakanpai(number)  # 玩家查看牌

    fagongpai(1, 3)  # 发第三轮公牌，1张
    chakanpai(number)  # 玩家查看牌

if __name__=="__main__":
    main()
