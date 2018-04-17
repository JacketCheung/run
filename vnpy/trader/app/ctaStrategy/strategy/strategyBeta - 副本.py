
# encoding: UTF-8

"""
这里的Demo是一个最简单的双均线策略实现，并未考虑太多实盘中的交易细节，如：
1. 委托价格超出涨跌停价导致的委托失败
2. 委托未成交，需要撤单后重新委托
3. 断网后恢复交易状态
4. 等等
这些点是作者选择特意忽略不去实现，因此想实盘的朋友请自己多多研究CTA交易的一些细节，
做到了然于胸后再去交易，对自己的money和时间负责。
也希望社区能做出一个解决了以上潜在风险的Demo出来。
"""

from __future__ import division

from vnpy.trader.vtConstant import EMPTY_STRING, EMPTY_FLOAT
from vnpy.trader.app.ctaStrategy.ctaTemplate import (CtaTemplate,
                                                     BarGenerator,
                                                     ArrayManager,

                                                      zhibiao
                                                     )
from datetime import datetime, time
########################################################################
class tempStrategy(CtaTemplate):
    """双指数均线策略Demo"""
    className = 'DoubleMaStrategy'
    author = u'用Python的交易员'

    # 策略参数
    fastWindow = 12     # 快速均线参数
    slowWindow = 26     # 慢速均线参数
    initDays = 0       # 初始化数据所用的天数

    # 策略变量
    fastMa0 = EMPTY_FLOAT   # 当前最新的快速EMA
    fastMa1 = EMPTY_FLOAT   # 上一根的快速EMA

    slowMa0 = EMPTY_FLOAT
    slowMa1 = EMPTY_FLOAT
    huice = False
    # 参数列表，保存了参数的名称
    paramList = ['name',
                 'className',
                 'author',
                 'vtSymbol',
                 'fastWindow',
                 'slowWindow']

    # 变量列表，保存了变量的名称
    varList = ['inited',
               'trading',
               'pos',
               'fastMa0',
               'fastMa1',
               'slowMa0',
               'slowMa1']

    # 同步列表，保存了需要保存到数据库的变量名称
    syncList = ['pos']


    #----------------------------------------------------------------------
    def __init__(self, ctaEngine, setting):
        """Constructor"""
        super(tempStrategy, self).__init__(ctaEngine, setting)
        self.bg = BarGenerator(self.onBar)
        self.am = ArrayManager()
        self.lastzhibiao = zhibiao(0,0,0)
        self.celve0 = zerocelve()
        # self.celve1 = ceshi()
        self.tickCelvezu = [self.celve0]
        self.barCelvezu = [self.celve0]

        self.tickadd = 1


        #断网恢复变量
        self.stopcount = None

        #交易时间和监控联网状态变量
        self.yepan = False
        self.yepanhour = None
        self.yepanminute = None
        self.lastbardatetime = None

        self.tradetime = None

        #控制开仓和平仓稳定变量
        self.tradecount = 0


        self.tradingcelve = [self.celve0]

        # 注意策略类中的可变对象属性（通常是list和dict等），在策略初始化时需要重新创建，
        # 否则会出现多个策略实例之间数据共享的情况，有可能导致潜在的策略逻辑错误风险，
        # 策略类中的这些可变对象属性可以选择不写，全都放在__init__下面，写主要是为了阅读
        # 策略时方便（更多是个编程习惯的选择）

    #----------------------------------------------------------------------
    def onInit(self):
        """初始化策略（必须由用户继承实现）"""
        self.writeCtaLog(u'双EMA演示策略初始化')

        initData = self.loadBar(self.initDays)
        for bar in initData:
            self.onBar(bar)
        self.am.inited = True
        self.putEvent()

    #----------------------------------------------------------------------
    def onStart(self):
        """启动策略（必须由用户继承实现）"""
        self.writeCtaLog(u'双EMA演示策略启动')
        self.putEvent()

    #----------------------------------------------------------------------
    def closeAllPosistion(self, price):
        print('--closeallpos--')
        if self.pos > 0:
            self.short(price - self.tickadd, abs(self.pos))
        elif self.pos < 0:
            self.cover(price + self.tickadd, abs(self.pos))

        # ----------------------------------------------------------------------
    def datetimePlusMinute(self, datelatime, minute):
        newdatetime = datetime.now()
        if datelatime.minute + minute < 60:
            newdatetime.minute = datelatime.minute + minute
        else:
            newdatetime.hour = datelatime.hour + 1
            newdatetime.minute = datelatime.minute + minute - 60
        return newdatetime

    # ----------------------------------------------------------------------
    def iscontinueTime(self, firstdatetime, seconddatetime):
        if (firstdatetime.hour == seconddatetime.hour and firstdatetime.minute + 1 == seconddatetime.minute) \
                or (
                firstdatetime.hour == seconddatetime.hour - 1 and firstdatetime.minute == 59 and seconddatetime.minute == 0):
            return True

    # ----------------------------------------------------------------------
    def isTradeContinueTime(self, firstdatetime, seconddatetime):
        if self.iscontinueTime(firstdatetime, seconddatetime):
            return True
        elif firstdatetime.hour == 10 and (
                firstdatetime.minute == 15 or firstdatetime.minute == 14) and seconddatetime.hour == 10 and seconddatetime.minute == 30:
            return True
        elif firstdatetime.hour == 11 and (
                firstdatetime.minute == 29 or firstdatetime.minute == 30) and seconddatetime.hour == 13 and seconddatetime.minute == 30:
            return True
        elif self.yepan:
            if firstdatetime.hour == self.yepanhour and (
                    firstdatetime.minute == self.yepanminute or firstdatetime.minute == self.yepanminute - 1) and seconddatetime.hour == 9 and seconddatetime.miute == 0:
                return True
        else:return False
    # ----------------------------------------------------------------------

    def tickcelve(self, zhibiao, price, tick):
        for celve in self.tickCelvezu:
            xinhao = celve.celveOntick(zhibiao, self.lastzhibiao)
            if xinhao == 100:
                print(price, 'kaicangduo', tick.datetime)
            if xinhao == 50:
                print(price, 'pingcang', tick.datetime)
            if xinhao == 200:
                print(price, 'kongcang', tick.datetime)
            if xinhao == 250:
                print (price, 'pingkongcang', tick.datetime)
            self.chulikaipingcang(xinhao, price)
            # ----------------------------------------------------------------------

    def barcelve(self, zhibiao, price):
        for celve in self.barCelvezu:
            xinhao = celve.celveOnbar(zhibiao, self.lastzhibiao)
            if xinhao == 100:
                print('kaicangduo,bar')
            if xinhao == 50:
                print('pingcang,bar')
            self.chulikaipingcang(xinhao, price)

    # ----------------------------------------------------------------------

    def chulikaipingcang(self, celve,price):
        # if celve == 100:
        #     self.buy(price,1)
        selfpos = 0
        if celve != 0 and celve is not None:
            print('nowposis',self.pos,'celveis',celve,'andpriceis',price)
        if self.pos == 0 and celve == 100:
            if self.pos == 0:
                # self.weituopos = 1
                self.buy(price + 100, 1)
                # 如果有空头持仓，则先平空，再做多
            elif self.pos < selfpos:
                # self.weituopos = 1
                self.cover(price, 1)
                self.buy(price, 1)
        elif self.pos == 1 and celve == 50:
            if self.pos > selfpos:
                # self.weituopos = 0
                self.sell(price - 1, 1)
        elif self.pos == 0 and celve == 200:
            if self.pos == selfpos:
                # self.weituopos = -1
                print('iamkonging')
                self.short(price - 1, 1)
            elif self.pos > selfpos:
                self.sell(price, 1)
                self.short(price, 1)
                # self.weituopos = -1
        elif self.pos == -1 and celve == 250:
                # self.weituopos += 1
                self.cover(price + 100, 1)
        # ----------------------------------------------------------------------

    def onStop(self):
        """停止策略（必须由用户继承实现）"""
        self.writeCtaLog(u'双EMA演示策略停止')
        self.putEvent()


    #----------------------------------------------------------------------
    def onTick(self, tick):
        """收到行情TICK推送（必须由用户继承实现）"""
        self.bg.updateTick(tick)
        zhibiao = self.am.updateTick(tick)
        if not self.tradecount:
            self.tickcelve(zhibiao,tick.lastPrice,tick)
        elif tick.datetime.second > 55 :
            print('in tradecount',tick.datetime)
            self.tickcelve(zhibiao,tick.lastPrice,tick)
    #----------------------------------------------------------------------
    def onBar(self, bar):
        """收到Bar推送（必须由用户继承实现）"""
        if bar.datetime.hour == 14 and bar.datetime.minute == 59:
            self.closeAllPosistion(bar.close)
        bartime = bar.datetime


        # 处理bar上的刚开仓
        self.handleTradeCount()



        if self.lastbardatetime is None:
            self.lastbardatetime = bar.datetime
        else :
            if not self.isTradeContinueTime(self.lastbardatetime,bar.datetime):
                #断网了，需要处理断网状态
                self.handleDisConnected(bar.close)
            #没有断网
            else:
                if self.stopcount > 0 :
                    self.stopcount -= 1






        am = self.am
        am.updateBar(bar)
        self.bg.updateBar(bar)
        # if not am.inited:
        #     print('retr')
           # return
        # 计算快慢均线
        self.celve0.nowtime = bar.datetime
        diff,dea,macd = am.diff,am.dea,am.macd
        jisuan = zhibiao(diff,dea,macd)
        self.barcelve(jisuan,bar.close)

        # 金叉和死叉的条件是互斥
        # 所有的委托均以K线收盘价委托（这里有一个实盘中无法成交的风险，考虑添加对模拟市价单类型的支持）

        self.lastzhibiao = am.endBar()
        # print self.lastzhibiao.diff,self.lastzhibiao.dea
        # 发出状态更新事件
        self.putEvent()

    #----------------------------------------------------------------------
    def handleTradeCount(self):
        if self.tradecount > 0:
            self.tradecount -= 1
    def onOrder(self, order):
        """收到委托变化推送（必须由用户继承实现）"""
        # 对于无需做细粒度委托控制的策略，可以忽略onOrder
        print 'order', order.price,order.direction,order.offset      ,order.orderTime
        pass

    #----------------------------------------------------------------------
    def onTrade(self, trade):
        """收到成交推送（必须由用户继承实现）"""
        # 对于无需做细粒度委托控制的策略，可以忽略onOrder\
        if trade.direction == u'多' and trade.offset == u'开仓':
            #self.sell(trade.price - 4, 1, stop=True)
            self.tradecount = 5
            print('kaiduo')
        if trade.direction == u'空' and trade.offset == u'开仓':
            #self.cover(trade.price + 4, 1, stop=True)
            self.tradecount = 5
            print('kaikong')

        if trade.direction == u'多' and trade.offset != u'开仓':
            self.cancelAll()
            self.celve0.cangwei += trade.volume
            print('pingkong')
        if trade.direction == u'空' and trade.offset != u'开仓':
            self.cancelAll()
            self.celve0.cangwei -= trade.volume
            print('pingduo')

        print 'trade',trade.price,trade.direction,trade.offset,trade.tradeTime
        pass

    #----------------------------------------------------------------------
    def onStopOrder(self, so):
        """停止单推送"""
        pass

    def handleDisConnected(self,price):
        print('DISCONNECTED')
        self.closeAllPosistion(price)
        self.stopcount = 15


#-----------------------------------------------------------
class celvemoban(object):
    # 100 代表多开，50 代表多平，200代表空开，250代表空平

    nowtime = None
    begintradetime = time(hour=9,minute=15)
    endtradetime = time(hour=14,minute=50)
    def __init__(self, tickadd=1.0):
        self.cangwei = 0
        self.caozuo = 0
        self.chicangjia = 0
        self.tickadd = tickadd
        self.canshu = 0.12 * tickadd
        self.lastzhibiao = None

    def cangweishibie(self, caozuo):
         if self.nowtime is not None and self.nowtime.time() > self.begintradetime and self.nowtime.time() < self.endtradetime:
            if self.cangwei == 0 and caozuo == duo:
                self.cangwei += 1
                return duo
            elif self.cangwei == 1 and caozuo == duoping:
                print('didduoping')
                self.cangwei -= 1
                return duoping
            elif self.cangwei == 0 and caozuo == kong:
                print('didkaikong')
                self.cangwei -= 1
                return kong
            elif self.cangwei == -1 and caozuo == kongping:
                self.cangwei += 1
                return kongping
            else:
                return 0
         elif caozuo == duoping :
             print('didduoping')
             self.cangwei -= 1
             return duoping
         elif caozuo == kongping:
             print('didkongping')
             self.cangwei += 1
             return kongping

    #----------------------------------------------------------------------

    def celveOntick(self, zhibiao, lastzhibiao):
        '''tick级策略'''
        raise NotImplemented

    def celveOnbar(self, zhibiao, lastzhibiao):
        '''bar策略'''
        raise NotImplemented
    def kaicang(self, zhibiao, lastzhibiao):
        '''符合准备条件后判断开仓'''

    def pingduo(self, zhibiao, lastzhibiao):
        '''平多仓'''
        if zhibiao.dj(lastzhibiao) == False:
            return duoping
        else:
            return 0

    def pingkong(self, zhibiao, lastzhibiao):
        '''平空仓'''
        if zhibiao.dj(lastzhibiao):
            return kongping
        else:
            return 0

    def kongcelve(self, zhibiao):
        '''tick级空策略'''

    def duocelve(self, zhibiao):
       '''tick级多策略'''



#----------------------------------------------------------------------------
class zerocelve(celvemoban):
    def __init__(self, tickadd=1):
        super(zerocelve, self).__init__()
        self.tiaojian = False

    def celveOntick(self, zhibiao, lastzhibiao):
        caozuo = 0
        if self.cangwei == 0 and self.tiaojian:
            # print('ont 1')
            caozuo = self.kaicang(zhibiao, lastzhibiao)
        elif self.cangwei > 0:
            # print('on 2')
            caozuo = self.pingduo(zhibiao, lastzhibiao)
        elif self.cangwei < 0:
            # print('on3')
            caozuo = self.pingkong(zhibiao, lastzhibiao)
        return self.cangweishibie(caozuo)

    def celveOnbar(self, zhibiao, lastzhibiao):
        self.fuhetiaojian(zhibiao)
        self.lastzhibiao = zhibiao

    def kaicang(self, zhibiao, lastzhibiao):
        if  lastzhibiao.inred():
            return self.kongcelve(zhibiao)
        else:
            return self.duocelve(zhibiao)

    def pingduo(self, zhibiao, lastzhibiao):
        if zhibiao.dj(lastzhibiao) == False:
            print('guesshoat')
            return duoping
        else:
            return 0

    def pingkong(self, zhibiao, lastzhibiao):
        if zhibiao.dj(lastzhibiao):
            return kongping
        else:
            return 0

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
#---------------------------------------------------------------------

class lianmiancelve(celvemoban):

    def celveOntick(self, zhibiao, lastzhibiao):
        '''tick级策略'''
        raise NotImplemented

    def celveOnbar(self, zhibiao, lastzhibiao):
        '''bar策略'''
        raise NotImplemented

    def kaicang(self, zhibiao, lastzhibiao):
        '''符合准备条件后判断开仓'''

    def pingduo(self, zhibiao, lastzhibiao):
        '''平多仓'''
        if zhibiao.dj(lastzhibiao) == False:
            return duoping
        else:
            return 0

    def pingkong(self, zhibiao, lastzhibiao):
        '''平空仓'''
        if zhibiao.dj(lastzhibiao):
            return kongping
        else:
            return 0

    def kongcelve(self, zhibiao):
        '''tick级空策略'''

    def duocelve(self, zhibiao):
        '''tick级多策略'''


duo = 100
duoping = 50
kong = 200
kongping = 250
kaipantime = time(hour=9, minute=0)
zaoxiutime = time(hour=10,minute=15)
zaoxiuendtime = time(hour=10,minute=30)
shoupantime = time(hour=15,minute=0)
wuxiutime = time(hour=11,minute=30)
zhongwukaipantime = time(hour=13,minute=30)

