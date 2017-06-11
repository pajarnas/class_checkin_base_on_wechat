#encoding=utf-8

from abc import ABCMeta, abstractmethod
import threading
from time import ctime
class Subject():
    __metaclass__ = ABCMeta
    observers=[]

    @abstractmethod
    def attach(self,observer):
        pass

    @abstractmethod
    def detach(self,observer):
        pass

    @abstractmethod
    def notify(self):
        pass

class Observer():
    __metaclass__ = ABCMeta
    def __init__(self):
        pass

    @abstractmethod
    def update(self):
        pass

if __name__=='__main__':
  pass

class TimeWindowObserver(Observer):
    def __init__(self,checkin_obj):
        Observer.__init__(self)
        self.checkin_obj = checkin_obj

    def update(self):
        # 问自己身上是否有计时器,有的话取消

        if isinstance(self.checkin_obj.time_window.t, threading._Timer) :
             self.checkin_obj.time_window.t.cancel()
             print 'cancel'

class EndcheckinObserver(Observer):
    def __init__(self,checkin_obj):
        Observer.__init__(self)
        self.checkin_obj = checkin_obj

    def update(self):
        if isinstance(self.checkin_obj.time_window.t, threading._Timer):
            print 'end checkin'
        # self.checkin_obj.end_checkin()
