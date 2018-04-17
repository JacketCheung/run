# encoding: UTF-8

"""
DualThrust交易策略
"""

from datetime import time

from vnpy.trader.vtObject import VtBarData
from vnpy.trader.vtConstant import EMPTY_STRING
from vnpy.trader.app.ctaStrategy.ctaTemplate import CtaTemplate, BarGenerator
from  vnpy.trader.app.ctaStrategy.strategy.strategyTemp import tempStrategy


########################################################################
class niStrategy(tempStrategy):
    def __init__(self,ctaEngine,setting,):
        super(niStrategy,self).__init__(ctaEngine,setting,10)