#encoding=utf-8

from abc import ABCMeta, abstractmethod
import threading,time

class Subject():
    __metaclass__ = ABCMeta
    def __init__(self):
        self.observers=[]

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
        # 只处理非正常结束计时器的考勤对象
        if isinstance(self.checkin_obj.time_window.t, threading._Timer) :
             self.checkin_obj.time_window.t.cancel()
             print 'cancel time :' + time.strftime('%H:%M:%S') +'__' +self.checkin_obj.tea_id
         

class EndcheckinObserver(Observer):
    def __init__(self,checkin_obj):
        Observer.__init__(self)
        self.checkin_obj = checkin_obj

    def update(self):
        print 'end checkin_files time :'+ time.strftime('%H:%M:%S') +'__' +self.checkin_obj.tea_id
        self.checkin_obj.end_checkin()


