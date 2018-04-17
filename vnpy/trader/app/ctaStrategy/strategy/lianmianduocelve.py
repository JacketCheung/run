# encoding: UTF-8
from celvemoban import celvemoban
from  datetime import  time

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

#-----------------------------------------------
class lianmianduocelve(celvemoban):
    def __init__(self,tickadd = 1):
        super(lianmianduocelve, self).__init__(tickadd)
        self.highestPrice = None
        self.highLowPrice = None
        self.highestMACD = None
        self.duotiaojian  = False
        self.celvename = 'lianmianduo'
        self.waves = 0
    def celveOntick(self, zhibiao):
        caozuo = 0
        if self.cangwei == 0:
            caozuo = self.duocelve(zhibiao)
        elif self.cangwei > 0 :
            caozuo = self.pingduo(zhibiao)
        return self.cangweishibie(caozuo)

    def celveOnbar(self, zhibiao):
        self.duopanduan(zhibiao)
        if self.tradePrice is not None:
            if self.cangwei > 0:
                self.barpingduo(zhibiao)
            elif self.cangwei < 0 :
                self.barpingkong(zhibiao)
    def duocelve(self, zhibiao):
        if zhibiao.macd > 0 :
            if self.duotiaojian and zhibiao.mj > 0 and zhibiao.macd < self.highestMACD * 1.0/3.0 and zhibiao.diff > self.canshu * 5:
                return  duo
            else: return  0


    def duopanduan(self, zhibiao):
        if zhibiao.macd < 0:
            self.huanyuanDuoShuXing()
        self.panduangaodian(zhibiao)
        if self.duotiaojian:
            if zhibiao.mj <0 :
                if zhibiao.lowArray[-1] < self.highLowPrice - 2 * self.tickadd:
                    self.duotiaojian = False

    def huanyuanDuoShuXing(self):
        self.duotiaojian = False
        self.highLowPrice = None
        self.highestPrice = None
        self.highestMACD = None

    def fuzhiDuo(self, zhibiao):
        # print('beve',zhibiao.datetime)
        self.duotiaojian = True
        self.highestMACD = zhibiao.lastmacd
        self.highLowPrice = zhibiao.low[-1]
        self.highestPrice = zhibiao.highArray[-2]

    def panduangaodian(self, zhibiao):
        if self.highestMACD is None:
            if zhibiao.mj < 0 and zhibiao.lastmj > 0 and zhibiao.lastmacd > 0 :
                self.fuzhiDuo(zhibiao)
        else:
            if zhibiao.mj < 0 and zhibiao.lastmj > 0 and zhibiao.lastmacd > 0 and self.highestPrice is not None and zhibiao.lastmacd > self.highestMACD and zhibiao.highArray[-2] > self.highestPrice :
                self.fuzhiDuo(zhibiao)
