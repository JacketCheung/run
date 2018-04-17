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

class lianmianKongcelve(celvemoban):
    def __init__(self,tickadd = 1,canshu = 4):
        super(lianmianKongcelve,self).__init__(tickadd)
        #做空所需属性
        self.lowestPrice = None
        self.lowHighPrice = None
        self.lowestMACD = None
        self.kongtiaojian = False
        self.celvename = 'lianmiankong'
        self.waves = 0
        self.secondlowPrice = None
        self.diefucanshu = canshu
        self.beginGreenPrice = None

    def celveOntick(self, zhibiao):
        '''tick级策略'''
        caozuo = 0
        if self.cangwei == 0:
           caozuo = self.kongcelve(zhibiao)
        elif self.cangwei > 0 :
           caozuo = self.pingkong(zhibiao)
        return self.cangweishibie(caozuo)


    def celveOnbar(self, zhibiao):
        '''bar策略'''
        self.kongpanduan(zhibiao)
        if self.tradePrice is not None:
            if self.cangwei < 0:
                self.barpingduo(zhibiao)
            elif self.cangwei > 0 :
                self.barpingkong(zhibiao)
    # def pingkong(self, zhibiao):
    #     '''平空仓'''
    #     if zhibiao.dj() > 0 and self.tradePrice is not None and self.tradePrice + 1 != zhibiao.close[-1] and self.tradePrice + 2 != zhibiao.close[-1] and self.tradePrice != zhibiao.close[-1] :
    #         print('pingkongcang',self.tradePrice,zhibiao.close[-1],zhibiao.close[-1])
    #         return kongping
    #     else:
    #         return 0

    def kongcelve(self, zhibiao):
        '''tick级空策略'''
        if zhibiao.macd < 0 :
            if self.kongtiaojian and zhibiao.mj < 0 and zhibiao.macd > self.lowestMACD * 1.0 / 3.0 and zhibiao.diff < 0 and zhibiao.close[-1] < self.secondlowPrice:
                #print('kaidkong','datetime',zhibiao.datetime,'mj',zhibiao.mj , 'macd',zhibiao.macd ,'lowestmacd',self.lowestMACD,'diff',zhibiao.diff,'close',zhibiao.close[-1],zhibiao.short,zhibiao.long)
                return duo
        else: return 0


    def kongpanduan(self, zhibiao):
        if zhibiao.macd > 0 :
            self.huanyuanKongShuXing()
        if zhibiao.macd < 0 and zhibiao.lastmacd > 0 :
            self.beginGreenPrice = zhibiao.open[-1]
        self.panduandidian(zhibiao)
        if self.kongtiaojian:
            if zhibiao.macd - zhibiao.lastmacd > 0:
                if zhibiao.highArray[-1] > self.lowHighPrice + 2 * self.tickadd:
                    self.kongtiaojian = False





    def huanyuanKongShuXing(self):
        self.kongtiaojian = False
        self.lowHighPrice = None
        self.lowestPrice = None
        self.lowestMACD = None

    def fuzhikong(self, zhibiao):
        # print('ever',zhibiao.datetime)
        self.kongtiaojian   = True
        self.lowestMACD = zhibiao.lastmacd
        self.lowHighPrice = zhibiao.high[-1]
        self.lowestPrice = zhibiao.lowArray[-2]
        self.secondlowPrice = zhibiao.close[-1]

    def panduandidian(self, zhibiao):
        if self.lowestMACD is None:
         if zhibiao.mj > 0 and zhibiao.lastmj < 0 and zhibiao.lastmacd < 0 and zhibiao.close[-1] < self.beginGreenPrice - self.diefucanshu * self.tickadd:
            self.fuzhikong(zhibiao)
        elif zhibiao.macd < 0 and self.lowestPrice is not None and zhibiao.mj > 0 and zhibiao.lastmj < 0 and zhibiao.lastmacd < self.lowestMACD and    zhibiao.lowArray[-2] < self.lowestPrice and  zhibiao.close[-1] < self.beginGreenPrice - self.diefucanshu * self.tickadd:
            self.fuzhikong(zhibiao)
