# -*- coding: utf-8 -*-
"""
Created on Fri May 29 02:50:00 2020

@author: wjize
"""
from pypokerengine.utils.card_utils import gen_cards,estimate_hole_card_win_rate
from pypokerengine.api.emulator import Emulator
from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.game_state_utils import restore_game_state, attach_hole_card, attach_hole_card_from_deck
import random as rand
import numpy as np
import pandas as pd
def win_rate_convert(win_rate):
    if win_rate>0.95:
        return 4
    elif win_rate>0.80:
        return 3
    elif win_rate>=0.55:
        return 2
    elif win_rate>0.33:
        return 1
    else:
        return 0
def card_convert(card):
    suit=card[:2]
    if(suit=='黑桃'):
        return 'S'+card[-1]
    elif(suit=='红桃'):
        return 'H'+card[-1]
    elif(suit=='方块'):
        return 'D'+card[-1]
    elif(suit=='梅花'):
        return 'C'+card[-1]
class MyModel(BasePokerPlayer):

    FOLD = 0
    CALL = 1
    MIN_RAISE = 2
    MAX_RAISE = 3

    def set_action(self, action):
        self.action = action
        self.first=action
        self.flag=1
    def declare_action(self, valid_actions, hole_card, round_state,ts=1):
        if(self.flag==1):
            self.flag=0
            pass
            if self.FOLD == self.action:
                return valid_actions[0]['action'], valid_actions[0]['amount']
            elif self.CALL == self.action:
                return valid_actions[1]['action'], valid_actions[1]['amount']
            elif self.MIN_RAISE == self.action:
                return valid_actions[2]['action'], valid_actions[2]['amount']['min']
            elif self.MAX_RAISE == self.action:
                return valid_actions[2]['action'], valid_actions[2]['amount']['max']
            else:
                raise Exception("Invalid action [ %s ] is set" % self.action)
        else:
            return self.__choice_action(valid_actions)
    def __choice_action(self, valid_actions):
        n=len(valid_actions)
        pos=1/n
        r = rand.random()
        if r <= pos:
            if(self.first==0):
                return valid_actions[0]['action'], valid_actions[0]['amount']
            elif self.first!=2:
                return valid_actions[self.first]['action'], valid_actions[self.first]['amount']
            else:
                return valid_actions[2]['action'], valid_actions[2]['amount']['min']
        elif r <= pos*2:
            return valid_actions[1]['action'], valid_actions[1]['amount']
        elif r <= pos*3:
            return valid_actions[2]['action'],valid_actions[2]['amount']['min']
        else:
            return valid_actions[2]['action'], valid_actions[2]['amount']['max']
    
class player:
    def __init__(self,name,chip,order,n=4):
        self.name=name
        self.chip=chip
        self.order=order
        self.hand=[]
        self.commit=[]
        self.n=n 
    def hole_card(self,cards):
        hold_card=[card_convert(i) for i in cards]
        self.hand=hold_card
    def commit_card(self,cards):
        commit_card=[card_convert(i) for i in cards]
        self.commit=commit_card
    def actions(self,actions):
        self.actions=actions
    def get_win_rate(self):
        win_rate=[]
        win_rate.append(estimate_hole_card_win_rate(1000,self.n,gen_cards(self.hand),[]))
        win_rate.append(estimate_hole_card_win_rate(1000,self.n,gen_cards(self.hand),gen_cards([self.commit[:3]])))
        win_rate.append(estimate_hole_card_win_rate(1000,self.n,gen_cards(self.hand),gen_cards([self.commit[:4]])))
        win_rate.append(estimate_hole_card_win_rate(1000,self.n,gen_cards(self.hand),gen_cards([self.commit[:]])))
        self.win_rate=win_rate
if __name__=='__main__':
    chip=int(input('输入初始筹码：'))
    order=int(input('输入顺序：'))
    
    main_player=player('group1',chip=chip,order=order)
    sb=int(input("请输入小盲:"))
    rounds=1
    r_n=4
    a=['Check' for i in range(10)]
    b=['Call' for i in range(10)]
    c=['2bet' for i in range(10)]
    d=['3bet' for i in range(10)]
    e=['4bet' for i in range(10)]
    f=['4bet' for i in range(10)]
    g=['C+bet' for i in range(10)]
    h=['C+2bet' for i in range(10)]
    j=['All_in' for i in range(10)]
    cols=['Check','Call',c[0],d[0],e[0],f[0],g[0],h[0],j[0]]
    wins=[np.nan for i in range(90)]
    df_1=pd.DataFrame({'names':['none' for i in range(90)],'active':a+b+c+d+e+f+g+h+j,'win_rate':wins})
    
    while (True and rounds<=5):
        a = input("如果游戏结束请输入0，否则输入任意数字:")
        if(a=='0'):
            break
        flag=float(input("如果是小盲则输入1，大盲输入2，否则输入0:"))
        hole_cards=input("请输入手牌，以英文逗号隔开，如: 红桃A,方块Q:").split(',')
        main_player.hole_card(hole_cards)
        win_rate=estimate_hole_card_win_rate(1000,main_player.n,gen_cards(main_player.hand),[])
        print(f'胜率为：{win_rate}')
        if(flag!=0):
            print(f'call 期望为：{win_rate*3.5*sb-(1-win_rate)*flag*sb}')
            print(f'2bet 期望为：{win_rate*3.5*sb+4*2*sb-(1-win_rate)*(flag+2)*sb}')
            print(f'3bet 期望为：{win_rate*3.5*sb+4*4*sb-(1-win_rate)*(flag+4)*sb}')
            print(f'4bet 期望为：{win_rate*3.5*sb+4*6*sb-(1-win_rate)*(flag+6)*sb}')
        else:
            print(f'call 期望为：{win_rate*3.5*sb+4*3*sb-(1-win_rate)*2*sb}')
            print(f'2bet 期望为：{win_rate*3.5*sb+4*2*sb-(1-win_rate)*(2+2)*sb}')
            print(f'3bet 期望为：{win_rate*3.5*sb+4*4*sb-(1-win_rate)*(2+4)*sb}')
            print(f'4bet 期望为：{win_rate*3.5*sb+4*6*sb-(1-win_rate)*(2+6)*sb}')
        ac=0
        acount=0
        while ac>=0:
            ac=float(input('下注金额：'))
            acount+=ac
        main_player.chip=main_player.chip-acount
        print(f'剩余筹码为：{main_player.chip}')
        r_n=int(input('输入剩余玩家人数：'))
        if(r_n==1):
            print('跑光了，本轮结束')
            rounds+=1
            continue
        main_player.commit+=([card_convert(i) for i in input("请输入公共牌，以英文逗号隔开，如: 红桃A,方块Q，黑桃3:").split(',')])
        win_rate=estimate_hole_card_win_rate(1000,main_player.n,gen_cards(main_player.hand),gen_cards(main_player.commit))
        print(f'胜率为：{win_rate}')
        ante=int(input('输入底注：'))
        print(f'call 期望为：{win_rate*ante+r_n*ac-(1-win_rate)*(acount+ac)}')
        print(f'2bet 期望为：{win_rate*ante+2*r_n*ac-(1-win_rate)*(acount+2*ac)}')
        print(f'3bet 期望为：{win_rate*ante+4*r_n*ac-(1-win_rate)*(acount+4*ac)}')
        print(f'4bet 期望为：{win_rate*ante+6*r_n*ac-(1-win_rate)*(acount+6*ac)}')
        ac=0
        acount=0
        while ac>=0:
            ac=float(input('下注金额：'))
            acount+=ac
        main_player.chip=main_player.chip-acount
        print(f'剩余筹码为：{main_player.chip}')
        r_n=int(input('输入剩余玩家人数：'))
        if(r_n==1):
            print('跑光了，本轮结束')
            rounds+=1
            continue
        main_player.commit.append(card_convert(input("请输入公共牌如: 红桃T:")))
        win_rate=estimate_hole_card_win_rate(1000,main_player.n,gen_cards(main_player.hand),gen_cards(main_player.commit))
        print(f'胜率为：{win_rate}')
        ante=int(input('输入底注：'))
        print(f'call 期望为：{win_rate*ante+r_n*ac-(1-win_rate)*(acount+ac)}')
        print(f'2bet 期望为：{win_rate*ante+2*r_n*ac-(1-win_rate)*(acount+2*ac)}')
        print(f'3bet 期望为：{win_rate*ante+4*r_n*ac-(1-win_rate)*(acount+4*ac)}')
        print(f'4bet 期望为：{win_rate*ante+6*r_n*ac-(1-win_rate)*(acount+6*ac)}')
        ac=0
        acount=0
        while ac>=0:
            ac=float(input('下注金额：'))
            acount+=ac
        main_player.chip=main_player.chip-acount
        print(f'剩余筹码为：{main_player.chip}')
        r_n=int(input('输入剩余玩家人数：'))
        if(r_n==1):
            print('跑光了，本轮结束')
            rounds+=1
            continue
        main_player.commit.append(card_convert(input("请输入公共牌如: 红桃T:")))
        win_rate=estimate_hole_card_win_rate(1000,main_player.n,gen_cards(main_player.hand),gen_cards(main_player.commit))
        print(f'胜率为：{win_rate}')
        ante=int(input('输入底注：'))
        print(f'call 期望为：{win_rate*ante+r_n*ac-(1-win_rate)*(acount+ac)}')
        print(f'2bet 期望为：{win_rate*ante+2*r_n*ac-(1-win_rate)*(acount+2*ac)}')
        print(f'3bet 期望为：{win_rate*ante+4*r_n*ac-(1-win_rate)*(acount+4*ac)}')
        print(f'4bet 期望为：{win_rate*ante+6*r_n*ac-(1-win_rate)*(acount+6*ac)}')
        ac=0
        acount=0
        while ac>=0:
            ac=float(input('下注金额：'))
            acount+=ac
        main_player.chip=main_player.chip-acount
        print(f'本局结束，剩余筹码为：{main_player.chip}')
        for i in range(2,5):
            add_name=[]
            add_active=[]
            add_win_rate=[]
            name_=input('总结时刻，输入玩家姓名')
            chip_=int(input('总结时刻，输入玩家剩余筹码'))
            order_=int(input('总结时刻，输入玩家序号'))
            if(name_=='-1'):
                continue
            player_=player(name_,chip=chip_,order=order_)
            hole_cards_=input("请输入该玩家手牌，以英文逗号隔开，如: 红桃A,方块Q:").split(',')
            player_.hole_card(hole_cards_)
            player_.commit=main_player.commit
            player_.get_win_rate()
            player_.actions=input('输入玩家每轮的行动，Check,SB,BB,Call,nbet,C+nbet,C+Fold，All_in 以英文逗号,分割：')
            index_=0
            for i in player_.actions:
                if i in cols:
                    add_name.append(name_)
                    add_active.append(i)
                    add_win_rate.append(win_rate_convert(player_.win_rate[index_]))
                    index_+=1
            pd.concat(df_1,pd.DataFrame({'names':add_name,'active':add_active,'win_rate':add_win_rate}))                  
        rounds+=1
        
    while (True):
        a = input("如果游戏结束请输入0，否则输入任意数字:")
        if(a=='0'):
            break
        flag=float(input("如果是小盲则输入1，大盲输入2，否则输入0:"))
        hole_cards=input("请输入手牌，以英文逗号隔开，如: 红桃A,方块Q:").split(',')
        main_player.hole_card(hole_cards)
        win_rate=estimate_hole_card_win_rate(1000,main_player.n,gen_cards(main_player.hand),[])
        print(f'胜率为：{win_rate}')
        if(flag!=0):
            print(f'call 期望为：{win_rate*3.5*sb-(1-win_rate)*flag*sb}')
            print(f'2bet 期望为：{win_rate*3.5*sb+4*2*sb-(1-win_rate)*(flag+2)*sb}')
            print(f'3bet 期望为：{win_rate*3.5*sb+4*4*sb-(1-win_rate)*(flag+4)*sb}')
            print(f'4bet 期望为：{win_rate*3.5*sb+4*6*sb-(1-win_rate)*(flag+6)*sb}')
        else:
            print(f'call 期望为：{win_rate*3.5*sb+4*3*sb-(1-win_rate)*2*sb}')
            print(f'2bet 期望为：{win_rate*3.5*sb+4*2*sb-(1-win_rate)*(2+2)*sb}')
            print(f'3bet 期望为：{win_rate*3.5*sb+4*4*sb-(1-win_rate)*(2+4)*sb}')
            print(f'4bet 期望为：{win_rate*3.5*sb+4*6*sb-(1-win_rate)*(2+6)*sb}')
        for name in set(list(df_1['name'].values)):
            if name=='none':
                continue
            print(name+'\'sinformtion:')
            ch_df=df_1[df_1['name'].isin(name)]
            ch_df=ch_df.drop_na()
            for ac in set(list(ch_df['active'])):
                props=ch_df['win_rate'][ch_df['active'].isin([ac])].values
                mean=np.nanmean(props[-5:])
                h_p=props[-5:][props[-5:]>=2]/len(props[-5:])
                print(ac+f' mean:{mean}   win_ratio:{h_p}\n')
        ac=0
        acount=0
        while ac>=0:
            ac=float(input('下注金额：'))
            acount+=ac
        main_player.chip=main_player.chip-acount
        print(f'剩余筹码为：{main_player.chip}')
        r_n=int(input('输入剩余玩家人数：'))
        if(r_n==1):
            print('跑光了，本轮结束')
            rounds+=1
            continue
        main_player.commit+=([card_convert(i) for i in input("请输入公共牌，以英文逗号隔开，如: 红桃A,方块Q，黑桃3:").split(',')])
        win_rate=estimate_hole_card_win_rate(1000,main_player.n,gen_cards(main_player.hand),gen_cards(main_player.commit))
        print(f'胜率为：{win_rate}')
        ante=int(input('输入底注：'))
        print(f'call 期望为：{win_rate*ante+r_n*ac-(1-win_rate)*(acount+ac)}')
        print(f'2bet 期望为：{win_rate*ante+2*r_n*ac-(1-win_rate)*(acount+2*ac)}')
        print(f'3bet 期望为：{win_rate*ante+4*r_n*ac-(1-win_rate)*(acount+4*ac)}')
        print(f'4bet 期望为：{win_rate*ante+6*r_n*ac-(1-win_rate)*(acount+6*ac)}')
        ac=0
        acount=0
        while ac>=0:
            ac=float(input('下注金额：'))
            acount+=ac
        main_player.chip=main_player.chip-acount
        print(f'剩余筹码为：{main_player.chip}')
        r_n=int(input('输入剩余玩家人数：'))
        if(r_n==1):
            print('跑光了，本轮结束')
            rounds+=1
            continue
        main_player.commit.append(card_convert(input("请输入公共牌如: 红桃T:")))
        win_rate=estimate_hole_card_win_rate(1000,main_player.n,gen_cards(main_player.hand),gen_cards(main_player.commit))
        print(f'胜率为：{win_rate}')
        ante=int(input('输入底注：'))
        print(f'call 期望为：{win_rate*ante+r_n*ac-(1-win_rate)*(acount+ac)}')
        print(f'2bet 期望为：{win_rate*ante+2*r_n*ac-(1-win_rate)*(acount+2*ac)}')
        print(f'3bet 期望为：{win_rate*ante+4*r_n*ac-(1-win_rate)*(acount+4*ac)}')
        print(f'4bet 期望为：{win_rate*ante+6*r_n*ac-(1-win_rate)*(acount+6*ac)}')
        ac=0
        acount=0
        while ac>=0:
            ac=float(input('下注金额：'))
            acount+=ac
        main_player.chip=main_player.chip-acount
        print(f'剩余筹码为：{main_player.chip}')
        r_n=int(input('输入剩余玩家人数：'))
        if(r_n==1):
            print('跑光了，本轮结束')
            rounds+=1
            continue
        main_player.commit.append(card_convert(input("请输入公共牌如: 红桃T:")))
        win_rate=estimate_hole_card_win_rate(1000,main_player.n,gen_cards(main_player.hand),gen_cards(main_player.commit))
        print(f'胜率为：{win_rate}')
        ante=int(input('输入底注：'))
        print(f'call 期望为：{win_rate*ante+r_n*ac-(1-win_rate)*(acount+ac)}')
        print(f'2bet 期望为：{win_rate*ante+2*r_n*ac-(1-win_rate)*(acount+2*ac)}')
        print(f'3bet 期望为：{win_rate*ante+4*r_n*ac-(1-win_rate)*(acount+4*ac)}')
        print(f'4bet 期望为：{win_rate*ante+6*r_n*ac-(1-win_rate)*(acount+6*ac)}')
        ac=0
        acount=0
        while ac>=0:
            ac=float(input('下注金额：'))
            acount+=ac
        main_player.chip=main_player.chip-acount
        print(f'本局结束，剩余筹码为：{main_player.chip}')
        for i in range(2,5):
            add_name=[]
            add_active=[]
            add_win_rate=[]
            name_=input('总结时刻，输入玩家姓名')
            chip_=int(input('总结时刻，输入玩家剩余筹码'))
            order_=int(input('总结时刻，输入玩家序号'))
            if(name_=='-1'):
                continue
            player_=player(name_,chip=chip_,order=order_)
            hole_cards_=input("请输入该玩家手牌，以英文逗号隔开，如: 红桃A,方块Q:").split(',')
            player_.hole_card(hole_cards_)
            player_.commit=main_player.commit
            player_.get_win_rate()
            player_.actions=input('输入玩家每轮的行动，Check,SB,BB,Call,nbet,C+nbet,C+Fold，All_in 以英文逗号,分割：')
            index_=0
            for i in player_.actions:
                if i in cols:
                    add_name.append(name_)
                    add_active.append(i)
                    add_win_rate.append(player_.win_rate[index_])
                    index_+=1
            pd.concat(df_1,pd.DataFrame({'names':add_name,'active':add_active,'win_rate':add_win_rate}))                  
        rounds+=1
    
        
            
