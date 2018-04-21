# encoding: UTF-8

"""
立即下载数据到数据库中，用于手动执行更新操作。

注意: 请先在本机启动天勤终端 (0.8.0 以上版本) 并保持运行, 再执行本程序
"""

from dataService import *



if __name__ == '__main__':
    symbols = 'SHFE.rb1810'
    downloadAllMinuteBar(1000, symbols)