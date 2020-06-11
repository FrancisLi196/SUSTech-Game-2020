
pai = [(20, '♠8'), (20, '♠9'),(28, '♣10'), (48, '♣J'), (40, '♣Q'), (18, '♣K'), (28, '♣A')]

'''
牌号值进行转换并将手上的牌排序-数字（赋值为1-13）和花色（1-4）
判断牌型级别
    判断是否皇家同花顺
        级别=900
    判断是否同花顺
        级别=800+牌面数字的权重
    判断是否四条
        ...
    判断是否葫芦
    判断是否同花
    判断是否顺子
    判断是否三条
    判断是否两对
    判断是否对子
    判断是否普通牌
判断每个玩家手上的最优牌型
比较不同玩家之间的大小
'''

#牌号值进行转换
def zhuanhuan(hand):
    global shuzi
    global huase
    shuzi = []
    huase = []
    for i in hand:
        shuzi.append((i[0]) % 13)
        huase.append((i[0]) // 13)
    #print(huase,shuzi)
    return shuzi, huase

#定义五项的组合
def combin(nums):
    from itertools import combinations
    result = []
    for i in combinations(nums,5):
        result.append(list(i))
    return result

#判断是否对子
def kind(n,pai):
    dui = []
    zhuanhuan(pai)
    for i in shuzi:
        shu = shuzi.count(i)
        if shu == n:
            if i in dui:
                continue
            dui.append(i)
    return dui

#判断牌型级别
def shunzi(pai):
    global jibie
    jibie = 0
    zhuanhuan(pai)

    '''
    #判断是否是高牌
    if max(shuzi) == 13 and len(set(shuzi)) == 5:
        jibie =jibie + 10**1
    '''

    #判断是否皇家同花顺
    if max(shuzi)- min(shuzi) == 4 and len(set(shuzi)) == 5 and len(set(huase)) == 1 and max(shuzi) == 12:
        jibie = 900
        return jibie

    #判断是否同花顺
    elif max(shuzi)- min(shuzi) == 4 and len(set(shuzi)) == 5 and len(set(huase)) == 1 and max(shuzi) != 13:
        jibie = 800 + max(shuzi)
        return jibie

    #判断是否四条
    elif len(kind(4, pai)) == 1:
        for i in shuzi:
            if i not in kind(4, pai):
                ti = i
        jibie = 700 + max(kind(4, pai)) + ti * 0.01
        return jibie

    #判断是否葫芦
    elif len(kind(3, pai)) == 1 and len(kind(2, pai)) == 1:
        jibie = 600 + max(kind(3, pai)) + max(kind(2, pai)) * 0.01
        return jibie

    #判断是否同花
    elif len(set(huase)) == 1:
        lin = list(shuzi)
        lin.sort(reverse=True)
        jibie = 500 + lin[0] + lin[1] * 0.01 + lin[2] * 0.0001 + lin[3] * 0.000001 + lin[4] * 0.00000001
        return jibie

    #判断是否顺子
    elif max(shuzi)- min(shuzi) == 4 and len(set(shuzi)) == 5 and max(shuzi) != 13:
            jibie = 400 + max(shuzi)
            return jibie

    #判断是否三条
    elif len(kind(3, pai)) == 1:
        lin = list(shuzi)
        lin.sort(reverse=True)
        ti = []
        for i in shuzi:
            if i not in kind(4, pai):
                ti.append(i)
        jibie = 300+ max(kind(3, pai)) + ti[0] * 0.01 + ti[1] * 0.0001
        return jibie

    #判断是否两对
    elif len(kind(2, pai)) == 2:
        for i in shuzi:
            if i != max(kind(2, pai)) and i != min(kind(2, pai)):
                ti = i
        jibie = 200 + max(kind(2, pai)) + min(kind(2, pai)) * 0.01 + ti * 0.0001
        return jibie

    # 判断是否对子
    elif len(kind(2, pai)) == 1:
        lin = list(shuzi)
        lin.sort(reverse=True)
        ti = []
        for i in shuzi:
            if i != max(kind(2, pai)):
                ti.append(i)
        jibie = 100+ max(kind(2, pai)) + ti[0] * 0.01 + ti[1] * 0.0001 + ti[2] * 0.000001
        return jibie

    # 判断是否普通牌
    else:
        lin = list(shuzi)
        lin.sort(reverse=True)
        jibie = 0 + lin[0] + lin[1] * 0.01 + lin[2] * 0.0001 + lin[3] * 0.000001 + lin[4] * 0.00000001
        return jibie
    #print(jibie)

#判断最优牌型
def zuiyou(pai):
    danji = []
    global jibie1
    jibie1 = 0
    for i in combin(pai):
        t=shunzi(i)
        #print(i,t)
        danji.append(t)
    jibie1 = max(danji)
    return(jibie1)
    #print(jibie1)

#判断最终牌型
def panduan(pai):
    '''
    print(combin(pai)[20])
    xin=combin(pai)[20]
    shunzi(xin)
    
    xin1=combin(pai)[18]
    danji.append(shunzi(xin1))
    print(xin1,shunzi(xin1))
    xin2=combin(pai)[19]
    danji.append(shunzi(xin2))
    print(xin2, shunzi(xin2))
    xin3=combin(pai)[20]
    danji.append(shunzi(xin3))
    print(xin3, shunzi(xin3))
    
    for i in range(len(combin(pai))):
        t=combin(pai)[i]
        n=shunzi(t)
        print(t,n,shunzi(t))
        danji.append(n)
    print(danji)
    jibie = max(danji)
    print(jibie)
    '''

    zuiyou(pai)
    global type
    if 100 <= jibie1 < 200:
        type = '对子'
    elif 200 <= jibie1 < 300:
        type = '两对'
    elif 300 <= jibie1 < 400:
        type = '三条'
    elif 400 <= jibie1 < 500:
        type = '顺子'
    elif 500 <= jibie1 < 600:
        type = '同花'
    elif 600 <= jibie1 < 700:
        type = '葫芦'
    elif 700 <=jibie1 < 800:
        type = '四条'
    elif 800 <= jibie1 < 900:
        type = '同花顺'
    elif 900 <= jibie1 < 1000:
        type = '皇家同花顺'
    else:
        type = '普通'
    return type
if __name__=="__main__":
    panduan(pai)
    print(type,jibie1)
'''
    if max(shuzi)- min(shuzi) == 4 and len(set(shuzi)) == 5:
        if len(set(huase)) == 1:
            if max(shuzi) == 12:
                print('皇家同花顺')
            else:
                print('同花顺')
        else:
            print('顺子')
    else:
        print('不是顺子')
'''
'''
number = []
for i in hand:
    huase = A[(i[0]-1) // 13]
    shuzi = B[(i[0]-1) % 13]
    number.append((i[0] + 2) % 13)
    print(huase + shuzi)
print(max(number))
print(min(number))
print(number)
'''
#if (max(hand)[0]-1) % 13 - (min(hand)[0]-1) % 13 == 4 and len(set(hand[0] % 13)) == 5:
#if max(hand)[0]-min(hand)[0]==4 and
'''
print('\n', max(pokername[i])[0])
print('\n', max(pokername[i]))
print(min(pokername[i])[0], '\n')
print(min(pokername[i]), '\n')
'''
'''
def straight(ranks):
  return (max(ranks) - min(ranks)) == 4 and len(set(ranks)) == 5

def flush(hand):
  suit = [s for r, s in hand]
  return len(set(suit)) == 1
def kind(n, ranks):
  for s in ranks:
    if ranks.count(s) == n : return s
  return None
'''
