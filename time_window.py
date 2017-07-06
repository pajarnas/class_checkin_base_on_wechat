#-*- coding=UTF-8 -*-


import threading
from checkin.printinfo import PrtInfo
from base_checkin import BaseCheckin


class TimeWindow:

    def __init__(self):
        self.t = None
        pass

    def just_waiting(self):
        # do noting
        pass

    def time_next(self):
        # 计时器保存t1,踢掉队首,并检查是否有t2
        # 如果有t2 , new一个新的计时器startTiming(t2 - t1)
        # 如果没有则startTiming():
        t1 = BaseCheckin.checkin_list[0].enter_time
        BaseCheckin.checkin_list[0].notify()
            # 通知观察者 考勤对象就要被踢掉了
        del BaseCheckin.checkin_list[0]
        if BaseCheckin.checkin_list != []:
            t2 = BaseCheckin.checkin_list[0].enter_time
            # dev = ((int(t2) - int(t1)) % 100) + ((int(t2) - int(t1)) / 100) * 60
            dev = self.dev(t1,t2)
            self.start_timing(dev)
        else:
            PrtInfo.tipsMessage(0)

    def time_second(self,t2, t3):
        dev = int(100) - self.dev(t2, t3)
        self.start_timing(dev)

    def start_timing(self, dev=6000):
        self.t = threading.Timer(dev, self.time_next)
        self.t.start()

    # 返回
    def dev(self, t2, t3):
        return (int(t3.split(':')[0]) - int(t2.split(':')[0])) * 60 + int(t3.split(':')[1]) - int(t2.split(':')[1])

if __name__ == '__main__':
    def dev( t2, t3):
        return (int(t3.split(':')[0]) - int(t2.split(':')[0])) * 60 + int(t3.split(':')[1]) - int(t2.split(':')[1])
    print dev('19:40','20:03')
    print dev('19:40', '20:37')
    print dev('19:40', '21:47')
    print  dev('19:40', '22:17')


