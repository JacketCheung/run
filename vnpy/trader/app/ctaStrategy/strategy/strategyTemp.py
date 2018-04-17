
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
from newzerocelve import newzerocelve
from zerocelve import zerocelve
from lianmianduocelve import lianmianduocelve
from lianmiankongcelve import lianmianKongcelve
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
    exitTime = time(hour=15, minute=0)

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
    def __init__(self, ctaEngine, setting,tickadd = 5):
        """Constructor"""
        super(tempStrategy, self).__init__(ctaEngine, setting)
        self.bg = BarGenerator(self.onBar)
        self.am = zhibiao()
        self.tickadd = tickadd


        #策略相关
        self.celve0 = zerocelve(self.tickadd)
        self.celve1 = lianmianKongcelve(self.tickadd)
        self.celve2 = lianmianduocelve(self.tickadd)
        self.celve3 = newzerocelve(self.tickadd,self.cancelAll)
        self.tickCelvezu = [
            #self.celve0,
            # self.celve1 ,
            self.celve3
                            ]
        self.barCelvezu = [#self.celve0 ,
           # ,self.celve2
            self.celve3
                           ]
        self.tradingcelve = [
            #self.celve0 ,
            #,self.celve2
            self.celve3
                             ]

        for ce in self.tradingcelve:
            ce.am = self.am
        #策略参数


        #断网恢复变量
        self.stopcount = None

        #交易时间和监控联网状态变量
        self.yepan = True
        self.yepanhour = 23
        self.yepanminute = 00
        self.lastbardatetime = None

        #交易变量相关
        self.tradetime = None

        #控制开仓和平仓稳定变量
        self.tradecount = 0



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
            pass
#            self.onBar(bar)
        self.am.inited = True

        self.putEvent()

    #----------------------------------------------------------------------
    def onStart(self):
        """启动策略（必须由用户继承实现）"""
        self.writeCtaLog(u'双EMA演示策略启动')
        self.putEvent()

    #----------------------------------------------------------------------
    def closeAllPosistion(self, price):
        self.cancelAll()
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
        elif self.yepan and (seconddatetime.hour == 9 or (seconddatetime.hour == 8 and seconddatetime.minute == 59)) and (
                    firstdatetime.hour == self.yepanhour or (
                    firstdatetime.hour == self.yepanhour - 1 and firstdatetime.minute == 59)):
                return True
        elif (firstdatetime.hour == 15 or (firstdatetime.hour == 14 and firstdatetime.minute ==59)) and ((seconddatetime.hour == 9 and seconddatetime.minute == 0) or (seconddatetime.hour == 8 and seconddatetime.minute == 59) ):
            return  True
        elif  ((firstdatetime.hour == 14 and firstdatetime.minute == 59) or firstdatetime.hour == 15 ) and (seconddatetime.hour == 21 or (seconddatetime.hour == 20 and seconddatetime.minute ==59)):
            return True
        else:
            print('dus conne',firstdatetime,seconddatetime)
            return False
    # ----------------------------------------------------------------------

    def tickcelve(self, zhibiao, price, tick):
        for celve in self.tickCelvezu:
            xinhao = celve.celveOntick(zhibiao)
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
            xinhao = celve.celveOnbar(zhibiao)
            if xinhao == 100:
                print('kaicangduo,bar')
            if xinhao == 50:
                print('pingcang,bar')
            self.chulikaipingcang(xinhao, price)

    # ----------------------------------------------------------------------

    def chulikaipingcang(self, celve,price):
        # if celve == 100:
        #     self.buy(price,1)
        print('chuli',celve,self.celve3.cangwei)
        selfpos = 0
        if celve != 0 and celve is not None:
            print('nowposis',self.pos,'celveis',celve,'andpriceis',price,self.am.datetime)
        if self.pos == 0 and celve == 100:
            if self.pos == 0:
                # self.weituopos = 1
                self.buy(price + 1, 1)
                # 如果有空头持仓，则先平空，再做多
            elif self.pos < selfpos:
                # self.weituopos = 1
                self.cover(price, 1)
                self.buy(price, 1)
        elif self.pos == 0 and celve == paiduikong:
            self.short(price ,1)
        elif self.pos == -1 and celve == paiduikongping:
            self.cover(price,1)
        elif self.pos == 1 and celve == 50:
            if self.pos > selfpos:
                # self.weituopos = 0
                self.sell(price - 1, 1)
        elif self.pos == 0 and celve == 200:
            if self.pos == selfpos:
                # self.weituopos = -1
                self.short(price - 1, 1)
            elif self.pos > selfpos:
                self.sell(price, 1)
                self.short(price, 1)
                # self.weituopos = -1
        elif self.pos == 0 and celve == paiduiduo:
            self.buy(price,1)
        elif self.pos > 0 and celve == paiduiduoping:
            self.sell(price,1)
        elif self.pos == -1 and celve == 250:
                # self.weituopos += 1
                self.cover(price + 1, 1)
        # ----------------------------------------------------------------------

    def onStop(self):
        """停止策略（必须由用户继承实现）"""
        self.writeCtaLog(u'双EMA演示策略停止')
        self.putEvent()


    #----------------------------------------------------------------------
    def onTick(self, tick):
        """收到行情TICK推送（必须由用户继承实现）"""
        self.bg.updateTick(tick)
        self.am.updateTick(tick)
        if not self.stopcount:
            if not self.tradecount:
                self.tickcelve(self.am,tick.lastPrice,tick)
            elif tick.datetime.second > 55 :
                self.tickcelve(self.am,tick.lastPrice,tick)
    #----------------------------------------------------------------------
    def onBar(self, bar):
        """收到Bar推送（必须由用户继承实现）"""
        print( 'begin')
        #过滤掉非交易时间的bar
        ntt = False
        if self.celve3.cancelorder is None and ntt:
            print('fuzhid')
            self.celve3.cancelorder = self.cancelOrder(self)
        else:
            ntt = True
        if self.notintradingTime(bar):
            return


        #数据合成和计算相关
        am = self.am
        am.updateBar(bar)
        self.bg.updateBar(bar)

        #处理是否断网
        self.checkIfConnecting(bar)


        # 处理bar上的刚开仓
        self.handleTradeCount()

        #检查是否断网所需的上一根bar时间
        self.lastbardatetime = bar.datetime




        # if not am.inited:
        #     print('retr')
           # return
        # 计算快慢均线

        #bar策略相关
        for ce in self.tradingcelve:
            ce.nowtime = bar.datetime
        if not self.stopcount:
            self.barcelve(am,bar.close)

        # 金叉和死叉的条件是互斥
        # 所有的委托均以K线收盘价委托（这里有一个实盘中无法成交的风险，考虑添加对模拟市价单类型的支持）

        am.endBar()
        # 发出状态更新事件
        self.putEvent()

    #----------------------------------------------------------------------
    def handleTradeCount(self):
        if self.tradecount > 0:
            self.tradecount -= 1
    def onOrder(self, order):
        """收到委托变化推送（必须由用户继承实现）"""
        # 对于无需做细粒度委托控制的策略，可以忽略onOrder
        self.celve3.order = order.vtOrderID
        print 'order', order.price,order.direction,order.offset      ,order.vtOrderID
        pass

    #----------------------------------------------------------------------
    def onTrade(self, trade):
        """收到成交推送（必须由用户继承实现）"""
        # 对于无需做细粒度委托控制的策略，可以忽略onOrder\
        if trade.direction == u'多' and trade.offset == u'开仓':
            self.tradecount = 5
           # print('kaiduo')
        if trade.direction == u'空' and trade.offset == u'开仓':
            self.tradecount = 5
          #  print('kaikong')

        if trade.direction == u'多' and trade.offset != u'开仓':
            self.cancelAll()
            print('slls',self.cancelAll() is None)
            self.celve2.cangwei = 0
          #  print('pingkong')
        if trade.direction == u'空' and trade.offset != u'开仓':
            self.cancelAll()
            self.celve2.cangwei = 0
            #self.celve0.cangwei -= trade.volume
           # print('pingduo')

        print 'trade',trade.price,trade.direction,trade.offset,trade.tradeTime


        #这里有待修正
        if trade.offset == u'开仓':
            for ce in self.tickCelvezu:
                print('set tradeprice')
                if ce.cangwei != 0:
                    ce.tradePrice = trade.price
        if trade.offset != u'开仓':
            for ce in self.tickCelvezu:
                if ce.cangwei == 0:
                    ce.tradePrice = None


    #----------------------------------------------------------------------
    def onStopOrder(self, so):
        """停止单推送"""
        pass

    def handleDisConnected(self,price):
        print('DISCONNECTED',self.lastbardatetime,self.am.datetime)
        self.closeAllPosistion(price)
        self.stopcount = 15

    def notintradingTime(self, bar):
        if bar.datetime.hour == 15 and bar.datetime.minute > 0:
            return True

    def closingTime(self, datetime):
        if datetime.hour == 14 and datetime.minute == 59:
            return True

    def checkIfConnecting(self,bar):
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
