# encoding: UTF-8

"""
导入MC导出的CSV历史数据到MongoDB中
"""
# encoding: UTF-8
#fb为螺纹1min主力
#te000 为镍主连
#tt0000 为pp主力
#kb0000 为rb主力
#ll为塑料主力
#bb为沥青主力
#a为铝主力
from vnpy.trader.app.ctaStrategy.ctaBase import MINUTE_DB_NAME,TICK_DB_NAME
from vnpy.trader.app.ctaStrategy.ctaHistoryData import loadMcCsv,loadqlCsv,load13Csv


if __name__ == '__main__':
     loadqlCsv('C:\Users\zpparker\Desktop\leapFTP\leapFTP\LeapFTP+3.0.1.46\l1805.csv', TICK_DB_NAME, 'lol000')
    #loadMcCsv('rb0000_1min.csv', MINUTE_DB_NAME, 'fb0000')

     # for i in [
     #           5,6,7,8,11,12,13,14,15,18,19,20,21,22,25,26,27,28,29
     #  ]:
     #      if i < 10:
     #           test = '2017120' + str(i)
     #      else:
     #           test = '201712' + str(i)
     #      #loadqlCsv('C:\Users\zpparker\Desktop\leapFTP\leapFTP\LeapFTP+3.0.1.46\\201712\\' + test + '\Tick\\bu1806.csv', TICK_DB_NAME, 'bb0000')
     #      #loadqlCsv('C:\Users\zpparker\Desktop\leapFTP\leapFTP\LeapFTP+3.0.1.46\\201712\\' + test + '\Tick\\l1805.csv', TICK_DB_NAME, 'll0000')
     #      loadqlCsv('C:\Users\zpparker\Desktop\leapFTP\leapFTP\LeapFTP+3.0.1.46\\201712\\' + test + '\Tick\\al1802.csv', TICK_DB_NAME, 'a0000')





