# encoding: UTF-8

from  datetime import  time
#-----------------------------------------------------------
class celvemoban(object):
    # 100 代表多开，50 代表多平，200代表空开，250代表空平

    nowtime = None
    begintradetime = time(hour=9,minute=00)
    endtradetime = time(hour=14,minute=50)
    def __init__(self, tickadd=1.0,cancel= None):
        self.cangwei = 0
        self.caozuo = 0
        self.chicangjia = 0
        self.tickadd = tickadd
        self.canshu = 0.12 * tickadd
        self.tradePrice = None
        self.celvename = 'moban'
        self.am = None
        self.order = None
        self.cancelorder = cancel
    def cangweishibie(self, caozuo):
         if self.nowtime is not None :
              #   and ( (self.nowtime.time() > self.begintradetime and self.nowtime.time() < self.endtradetime) or (self.nowtime.time() > time(hour=21,minute= 05)))\
            if self.cangwei == 0 and caozuo == duo:
                self.cangwei += 1
                print('xinhaonameis', self.celvename,'duo')
                return duo
            elif self.cangwei == 1 and caozuo == duoping:
                print('xinhaonameis', self.celvename,'duoping')
                self.cangwei -= 1
                return duoping
            elif self.cangwei == 0 and caozuo == kong:
                print('xinhaonameis', self.celvename,'kong')
                self.cangwei -= 1
                return kong
            elif self.cangwei == -1 and caozuo == kongping:
                self.cangwei += 1
                print('xinhaonameis', self.celvename,'kongping')

                return kongping
            elif self.cangwei == 0 and caozuo == paiduikong:
                self.cangwei -= 1
                return paiduikong
            elif  self.cangwei  == -1 and caozuo == paiduikongping:
                self.cangwei = 0
                return paiduikongping
            elif self.cangwei == 0 and caozuo  == paiduiduo:
                self.cangwei += 1
                return paiduiduo
            elif self.cangwei > 0 and caozuo == paiduiduoping:
                self.cangwei -= 1
                return paiduiduoping
         elif caozuo == duoping :
             print('xinhaonameis', self.celvename,'duoping')
             self.cangwei -= 1
             return duoping
         elif caozuo == kongping:
             print('xinhaonameis', self.celvename,'kongping')
             self.cangwei += 1
             return kongping
         elif  self.cangwei  == -1 and caozuo == paiduikongping:
            self.cangwei += 1
            self.cangwei = 0
            return paiduikongping
         elif self.cangwei > 0 and caozuo == paiduiduoping:
            self.cangwei -= 1
            return paiduiduoping
         return  0
    #----------------------------------------------------------------------

    def celveOntick(self, zhibiao,tick = None):
        '''tick级策略'''
        raise NotImplemented

    def celveOnbar(self, zhibiao):
        '''bar策略'''
        raise NotImplemented
    def kaicang(self, zhibiao):

        '''符合准备条件后判断开仓'''
    def onTrade(self):
        pass
    def barpingduo(self,zhibiao):
        lirun = self.duolirun(zhibiao)
        if lirun != -1 * self.tickadd and lirun != self.tickadd * -2 and lirun != 0:
            if zhibiao.mj < 0 and lirun < 6 * self.tickadd:
                return duoping
        return  0
    def barpingkong(self,zhibiao):
        lirun = self.duolirun(zhibiao)
        if lirun != -1 * self.tickadd and lirun != self.tickadd * -2 and lirun != 0:
            if zhibiao.mj > 0 and lirun < 6 * self.tickadd:
                return kongping
        return 0
    def pingduo(self, zhibiao):
        '''平多仓'''
        if self.tradePrice is not None:
            lirun = self.duolirun(zhibiao)
            if lirun != 0 and lirun != -1 * self.tickadd and lirun != -2 * self.tickadd:
                if zhibiao.dj()  < 0:
                    return duoping
        return 0

    def pingkong(self, zhibiao):
        '''平空仓'''
        if self.tradePrice is not None:
            lirun = self.konglirun(zhibiao)
            if lirun != 0 and lirun != -1 * self.tickadd and lirun != -2 * self.tickadd:
               if zhibiao.dj() > 0:
                    return kongping
        return 0

    def kongcelve(self, zhibiao):
        '''tick级空策略'''

    def duocelve(self, zhibiao):
       '''tick级多策略'''

    def konglirun(self, zhibiao):
        return self.tradePrice - zhibiao.close[-1]
    def duolirun(self,zhibiao):
        # print('lirun',)

        return zhibiao.close[-1] - self.tradePrice


#----------------------------------------------------------------------------


#---------------------------------------------------------------------



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

