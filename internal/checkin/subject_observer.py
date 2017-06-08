#encoding=utf-8

from abc import ABCMeta, abstractmethod

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

