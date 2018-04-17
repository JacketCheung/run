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
                                                     ArrayManager)


########################################################################
class DoubleMaStrategy(CtaTemplate):
    """双指数均线策略Demo"""
    className = 'DoubleMaStrategy'
    author = u'用Python的交易员'
    
    # 策略参数
    fastWindow = 12     # 快速均线参数
    slowWindow = 26     # 慢速均线参数
    initDays = 10       # 初始化数据所用的天数
    
    # 策略变量
    fastMa0 = EMPTY_FLOAT   # 当前最新的快速EMA
    fastMa1 = EMPTY_FLOAT   # 上一根的快速EMA
    
    slowMa0 = EMPTY_FLOAT
    slowMa1 = EMPTY_FLOAT
    
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
        super(DoubleMaStrategy, self).__init__(ctaEngine, setting)
        
        self.bg = BarGenerator(self.onBar)
        self.am = ArrayManager()
        self.lastzhibiao = zhibiao()
        self.celve0 = zerocelve()
        self.tickCelvezu = [celve0]
        self.barCelvezu = [celve0]
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
        
        self.putEvent()
        
    #----------------------------------------------------------------------
    def onStart(self):
        """启动策略（必须由用户继承实现）"""
        self.writeCtaLog(u'双EMA演示策略启动')
        self.putEvent()
    
    #----------------------------------------------------------------------
    def onStop(self):
        """停止策略（必须由用户继承实现）"""
        self.writeCtaLog(u'双EMA演示策略停止')
        self.putEvent()
        
    #----------------------------------------------------------------------
    def tickcelve(self,zhibiao):
        for celve in self.tickCelvezu:
          self.chulikaipingcang(celve.celveOntick(zhibiao,self.lastzhibiao),tick)
    def barcelve(self,zhibiao):
        for celve in self.barCelvezu:
           self.chulikaipingcang( celve.celveOnbar(zhibiao,self.lastzhibiao),None,bar)
    #----------------------------------------------------------------------
    def onTick(self, tick):
        """收到行情TICK推送（必须由用户继承实现）"""
        self.bg.updateTick(tick)
        zhibiao = self.am.updateTick(tick)
        self.tickcelve(zhibiao)
    #----------------------------------------------------------------------
    def onBar(self, bar):
        """收到Bar推送（必须由用户继承实现）"""
        am = self.am        
        am.updateBar(bar)
        if not am.inited:
            return
        
        # 计算快慢均线
        zhibiao = zhibiao(am.MACD(12,26,9))
        self.barcelve(zhibiao)

        
        # 金叉和死叉的条件是互斥
        # 所有的委托均以K线收盘价委托（这里有一个实盘中无法成交的风险，考虑添加对模拟市价单类型的支持）

        self.lastzhibiao = am.endBar()
        # 发出状态更新事件
        self.putEvent()
        
    #----------------------------------------------------------------------
    def onOrder(self, order):
        """收到委托变化推送（必须由用户继承实现）"""
        # 对于无需做细粒度委托控制的策略，可以忽略onOrder
        pass
    
    #----------------------------------------------------------------------
    def onTrade(self, trade):
        """收到成交推送（必须由用户继承实现）"""
        # 对于无需做细粒度委托控制的策略，可以忽略onOrder
        pass
    
    #----------------------------------------------------------------------
    def onStopOrder(self, so):
        """停止单推送"""
        pass
class celvemoban(object):
    # 100 代表多开，50 代表多平，200代表空开，250代表空平

    def __init__(self,tickadd = 1):
        self.cangwei = 0
        self.caozuo = 0
        self.chicangjia = 0
        self.tickadd = tickadd
        self.canshu = 0.12 * tickadd
    def cangweishibie(self,caozuo):
        if self.cangwei == 0 and caozuo == 100:
            self.cangwei += 1
            return 100
        elif self.cangwei == 1 and caozuo == 50:
            self.cangwei -= 1
            return 50
        else: return 0
class ceshi(celvemoban):
    def celve(self,macd,lastmacd):
        caozuo = 0
        if  macd > 0 and lastmacd < 0 :
            caozuo = self.cangweishibie(duo)
        if macd < 0 and lastmacd > 0:
            caozuo = self.cangweishibie(duoping)
class zerocelve(celvemoban):
    def __init__(self,tickadd = 1):
        super.__init__()
        self.tiaojian = False
    def celveOntick(self,zhibiao,lastzhibiao):
        caozuo =0
        if self.cangwei == 0 and self.tiaojian:
            caozuo = self.kaicang(zhibiao,lastzhibiao)
        elif self.cangwei > 0:
            caozuo =self.pingduo(zhibiao,lastzhibiao)
        elif self.cangwei < 0:
            caozuo = self.pingkong(zhibiao,lastzhibiao)
        return self.cangweishibie(caozuo)

    def celveOnbar(self, zhibiao):
        self.fuhetiaojian(zhibiao)
    def kaicang(self,zhibiao,lastzhibiao):
        if lastzhibiao.inred():
            return self.kongcelve(zhibiao)
        else:
            return self.duocelve(zhibiao)
    def pingduo(self, zhibiao, lastzhibiao):
        if not zhibiao.dj(lastzhibiao):
            return duoping
        else:
            return 0
    def pingkong(self,zhibiao,lastzhibiao):
        if zhibiao.dj(lastzhibiao):
            return kongping
        else: return 0
    def kongcelve(self,zhibiao):
        if self.moban(zhibiao,False):
            return kong
        else:return 0

    def duocelve(self,zhibiao):
        if self.moban(zhibiao,True):
            return duo
        else:return 0
    def moban(self,zhibiao,fangxiang):
        fanhuizhi = False
        if zhibiao.macd * fangxiang > 0:
            fanhuizhi = True
        return fanhuizhi
    def fuhetiaojian(self, zhibiao):
        if zhibiao is not None and zhibiao.dea < self.canshu and zhibiao.dea > -self.canshu:
            self.tiaojian = True
        else:
            self.tiaojian =  False

duo = 100
duoping = 50
kong = 200
kongping = 250
class zhibiao():
    def __init__(self,diff,dea,macd):
        self.diff = diff
        self.dea = dea
        self.macd = macd
    def inred(self):
        return self.macd > 0
    def dj(self,lastzhibiao):
        return self.diff - lastzhibiao.diff