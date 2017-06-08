#-*- coding=UTF-8 -*-


import threading
from printinfo import PrtInfo
from base_checkin import BaseCheckin


class Timer:

    t = None

    def __init__(self):
        pass

    def just_waiting(self):
        # do noting
        pass

    def time_next(self):
        # 计时器保存t1,踢掉队首,并检查是否有t2
        # 如果有t2 , new一个新的计时器startTiming(t2 - t1)
        # 如果没有则startTiming():
        print 'time is 15'
        t1 = BaseCheckin.checkin_list[0].enter_time
        BaseCheckin.checkin_list[0].notify()
        # checkin.checkin_list[0].time_window.t.cancle()
        # 通知观察者 考勤对象就要被踢掉了
        del BaseCheckin.checkin_list[0]
        if BaseCheckin.checkin_list != []:
            t2 = BaseCheckin.checkin_list[0].enter_time
            # dev = ((int(t2) - int(t1)) % 100) + ((int(t2) - int(t1)) / 100) * 60
            dev = self.dev(t1,t2)
            self.start_timing(dev)
        else:
            PrtInfo.tipsMessage(0)

    def time_second(self,t2,t3):
        # 队首被新来的踢了, 且新来的不是新队首时, 直接调用这个函数, 获取t2, t3
        # 然后startTiming(100 + t3 - t2)
        dev =int(100) - self.dev(t2,t3)
        print 'in time window'
        print dev
        self.start_timing(dev)

    def start_timing(self, dev=100):
        self.t = threading.Timer(dev, self.time_next)
        self.t.start()

    def dev(self, t2, t3):
        return (int(t3.split(':')[0]) - int(t2.split(':')[0])) * 60 + \
               int(t3.split(':')[1]) - int(t2.split(':')[1])

if __name__ == '__main__':
   pass



