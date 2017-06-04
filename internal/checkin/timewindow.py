#-*- coding=UTF-8 -*-


import threading
from printinfo import PrtInfo
from checkin import Checkin
class Timer():

    t = None
    def __init__(self):
        pass


    def justWaiting(self):
        # do noting
        pass

    def timeNext(self):
        # 计时器保存t1,踢掉队首,并检查是否有t2
        # 如果有t2 , new一个新的计时器startTiming(t2 - t1)
        # 如果没有则startTiming():
        t1 = Checkin.checkin_list[0].enter_time
        del Checkin.checkin_list[0]
        if Checkin.checkin_list != []:
            t2 = Checkin.checkin_list[1].enter_time
            dev = ((int(t2) - int(t1)) % 100) + ((int(t2) - int(t1)) / 100) * 60
            self.startTiming(dev)
        else:
            PrtInfo.tipsMessage(0)

    def timeSecond(self,t2,t3):
        # 队首被新来的踢了, 且新来的不是新队首时, 直接调用这个函数, 获取t2, t3
        # 然后startTiming(100 + t3 - t2)
        self.startTiming(100 + t3 - t2)

    def startTiming(self, dev=100):
        self.t = threading.Timer(dev, self.timeNext)
        self.t.start()

if __name__ == '__main__':
   pass



