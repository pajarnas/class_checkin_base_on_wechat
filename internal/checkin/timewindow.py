#-*- coding=UTF-8 -*-


import threading
from printinfo import PrtInfo
from checkin import Checkin
class Timer():

    def __init__(self):
        self.t = None

    def clearList(self):
         Checkin.checkin_list = []
         self.shutDownTimerThreading()

    def startTimerThreading(self,dev_time):
        if self.t != None:
            self.shutDownTimerThreading()
        self.t = threading.Timer(dev_time,self.clearList)
        PrtInfo.successMessage(10)
        self.t.start()

    def shutDownTimerThreading(self):
        PrtInfo.successMessage(9)
        self.t.cancel()

if __name__ == '__main__':
   pass



