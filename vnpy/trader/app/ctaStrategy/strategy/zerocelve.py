# encoding: UTF-8
from celvemoban import celvemoban
from datetime import time
class zerocelve(celvemoban):
    def __init__(self, tickadd=1):
        super(zerocelve, self).__init__()
        self.tiaojian = False
        self.celvename = '0'

    def celveOntick(self, zhibiao):
        caozuo = 0
        if self.cangwei == 0 and self.tiaojian:
            # print('ont 1')
            caozuo = self.kaicang(zhibiao)
        elif self.cangwei > 0 :
            # print('on 2')
            caozuo = self.pingduo(zhibiao)
        elif self.cangwei < 0  :
            # print('on3')
            caozuo = self.pingkong(zhibiao)
        return self.cangweishibie(caozuo)

    def celveOnbar(self, zhibiao):
        self.fuhetiaojian(zhibiao)
        if self.tradePrice!= None:
            if self.cangwei > 0:
                self.barpingduo(zhibiao)
            elif self.cangwei < 0 :
                self.barpingkong(zhibiao)

    def kaicang(self, zhibiao):
        if  zhibiao.lastmacd > 0:
            return self.kongcelve(zhibiao)
        else:
            return self.duocelve(zhibiao)

    # def pingduo(self, zhibiao):
    #     if zhibiao.dj() < 0 :
    #         if self.tradePrice is not None and zhibiao.close[-1] != self.tradePrice - 1 and zhibiao.close[-1] != self.tradePrice - 2 and zhibiao.close[-1] != self.tradePrice:
    #           return duoping
    #     else:
    #         return 0

    # def pingkong(self, zhibiao):
    #     if zhibiao.dj() > 0 :
    #         if self.tradePrice is not None and zhibiao.close[-1] != self.tradePrice + 1 and zhibiao.close[-1] != self.tradePrice + 2 and zhibiao.close[-1] != self.tradePrice:
    #             return kongping
    #     else:
    #         return 0

    def kongcelve(self, zhibiao):
        if zhibiao.macd < 0:
            return kong
        else:
            return 0

    def duocelve(self, zhibiao):
        if self.moban(zhibiao, True):
            return duo
        else:
            return 0

    def moban(self, zhibiao, fangxiang):
        fanhuizhi = False
        if zhibiao.macd * fangxiang > 0:
            fanhuizhi = True
        return fanhuizhi

    def fuhetiaojian(self, zhibiao):
        if zhibiao is not None and zhibiao.dea < self.canshu and zhibiao.dea > -self.canshu:
            self.tiaojian = True

        else:
            self.tiaojian = False
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