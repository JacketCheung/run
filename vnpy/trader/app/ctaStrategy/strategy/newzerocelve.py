# encoding: UTF-8
from celvemoban import celvemoban
from  datetime import  time
#----------------------------
duo = 100
duoping = 50
paiduiduo = 150
paiduiduoping = 155
kong = 200
kongping = 250
paiduikong = 400
paiduikongping = 500
kaipantime = time(hour=9, minute=0)
zaoxiutime = time(hour=10,minute=15)
zaoxiuendtime = time(hour=10,minute=30)
shoupantime = time(hour=15,minute=0)
wuxiutime = time(hour=11,minute=30)
zhongwukaipantime = time(hour=13,minute=30)

class newzerocelve(celvemoban):
    def celveOntick(self, zhibiao):

        caozuo = 0
        if self.am.tick.datetime.second > 50:
            if self.cangwei == 0 and self.tradePrice is None:
                if zhibiao.diff > 0 and zhibiao.lastmacd > 0 and zhibiao.macd < 0:
                    return self.cangweishibie(paiduiduo)
                elif zhibiao.diff < 0 and zhibiao.lastmacd < 0 and zhibiao.macd > 0:
                    return self.cangweishibie(paiduikong)
            elif self.cangwei > 0:
                if zhibiao.macd > 0:
                    if self.tradePrice is not None:
                        return self.cangweishibie(paiduiduoping)
                    else:
                        print('cancel duo',zhibiao.tick.datetime)
                        self.cancelorder()
            elif self.cangwei < 0:
                if zhibiao.macd < 0 and zhibiao.mj< 0:
                    if self.tradePrice is not None:
                        return self.cangweishibie(paiduikongping)
                    else:
                        print('cancel kong',zhibiao.tick.datetime,self.order)
                        self.cancelorder()
                else:
                    if zhibiao.macd < 0 and zhibiao.mj > 0 :
                        return self.cangweishibie(kongping)
    def celveOnbar(self, zhibiao):
        pass


