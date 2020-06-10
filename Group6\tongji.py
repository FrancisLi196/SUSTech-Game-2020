import random
import time
number = int(input('请输入玩家人数：'))


A=['♥','♠','♦','♣']
B=['3','4','5','6','7','8','9','10','J','Q','K','A','2']
poker=[]

n=1
for i in A:
    for j in B:
         poker.append((n,(i+j)))
         n=n+1
#print("开始洗牌....")
#print(poker)
pokers=poker.copy( )




#定义洗牌
def xipai(x):
    for i in x:
        pokers.remove(i)
    return pokers

#定义发牌
def fapai(y):
    for i in y:
        print(i[1],',',end=" ")


# 牌号值进行转换
def zhuanhuan(hand):
    global shuzi
    global huase
    shuzi = []
    huase = []
    for i in hand:
        shuzi.append((i[0]) % 13)
        huase.append((i[0]) // 13)
    # print(huase,shuzi)
    return shuzi, huase


# 定义五项的组合
def combin(nums):
    from itertools import combinations
    result = []
    for i in combinations(nums, 5):
        result.append(list(i))
    return result


# 判断是否对子
def kind(n, pai):
    dui = []
    zhuanhuan(pai)
    for i in shuzi:
        shu = shuzi.count(i)
        if shu == n:
            if i in dui:
                continue
            dui.append(i)
    return dui


# 判断牌型级别
def shunzi(pai):
    global jibie
    jibie = 0
    zhuanhuan(pai)
    # 判断是否是高牌
    '''
    if max(shuzi) == 13 and len(set(shuzi)) == 5:
        jibie =jibie + 10**1
    '''

    # 判断是否皇家同花顺
    if max(shuzi) - min(shuzi) == 4 and len(set(shuzi)) == 5 and len(set(huase)) == 1 and max(shuzi) == 12:
        jibie = 900
        return jibie

    # 判断是否同花顺
    elif max(shuzi) - min(shuzi) == 4 and len(set(shuzi)) == 5 and len(set(huase)) == 1 and max(shuzi) != 13:
        jibie = 800
        return jibie

    # 判断是否四条
    elif len(kind(4, pai)) == 1:
        jibie = 700
        return jibie

    # 判断是否葫芦
    elif len(kind(3, pai)) == 1 and len(kind(2, pai)) == 1:
        jibie = 600
        return jibie

    # 判断是否同花
    elif len(set(huase)) == 1:
        jibie = 500
        return jibie

    # 判断是否顺子
    elif max(shuzi) - min(shuzi) == 4 and len(set(shuzi)) == 5 and max(shuzi) != 13:
        jibie = 400
        return jibie

    # 判断是否三条
    elif len(kind(3, pai)) == 1:
        jibie = 300
        return jibie

    # 判断是否两对
    elif len(kind(2, pai)) == 2:
        jibie = 200
        return jibie

    # 判断是否对子
    elif len(kind(2, pai)) == 1:
        jibie = 100
        return jibie
    else:
        return jibie
    # print(jibie)


# 判断最终牌型
def panduan(pai):
    type = ''
    danji = []
    for i in combin(pai):
        t = shunzi(i)
        # print(i,t)
        danji.append(t)
    jibie = max(danji)
    # print(jibie)
    if 100 <= jibie < 200:
        type = '对子'
    elif 200 <= jibie < 300:
        type = '两对'
    elif 300 <= jibie < 400:
        type = '三条'
    elif 400 <= jibie < 500:
        type = '顺子'
    elif 500 <= jibie < 600:
        type = '同花'
    elif 600 <= jibie < 700:
        type = '葫芦'
    elif 700<= jibie < 800:
        type = '四条'
    elif 800 <= jibie < 900:
        type = '同花顺'
    elif 900 <= jibie < 1000:
        type = '皇家同花顺'
    else:
        type = '普通'
    return type

#定义函数：每个人发5张牌
def fadipai(number):
    #time.sleep(3)
    global pokers
    pokers = poker.copy( )
    global pokername
    random.shuffle(pokers)
    #print(pokers)
    #print(pokers)
    pokername = []
    for i in range(number):
        pokername.append(random.sample(pokers,5))
        pokers = xipai(pokername[i])
        #print("\n开始给player{}发牌：".format(i+1))
        #fapai(pokername[i])
        pokername[i].sort()

dict = {}
#定义函数：玩家轮流查看底牌
def chakanpai(number):
    fadipai(number)  # 发底牌
    #print('\n')
    for i in range(number):
        print("player{}的牌：".format(i+1))
        fapai(pokername[i])
        paixing = panduan(pokername[i])
        print(paixing)
        #if paixing not in dict:
        if paixing in dict:
            dict[paixing] = dict[paixing] + 1
        else:
            dict[paixing] = 1
        #print(dict)
    return dict
num = int(input('输入执行次数：'))
for i in range(num+1):
    print('\n第{}轮：'.format(i))
    chakanpai(number)#玩家查看牌
print(dict)
gailv = {}
for i in dict:
    gailv[i] = str(dict[i] / (num * number) * 100) + '%'
print(gailv)
