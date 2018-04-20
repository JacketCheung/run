import os
import time
def runCheckNetwork():
    while True:
        status = os.system('ping www.baidu.com')
        if status == 1:
            os.system('netsh wlan connect name = pakerPhone ')

        time.sleep(60)
if __name__ == '__main__':
    runCheckNetwork()
