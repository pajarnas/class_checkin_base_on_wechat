import time,threading

def p():
    print type(i)
list = []
for i in range(3):
    l = threading.Timer(5,p)
    l.start()
    list.append(l)

list.append(None)
list.append(None)
time.sleep(1)
for i in list:
    print type(i)



for i in list:
    if i is not None:
        if isinstance(i, threading._Timer):
            i.cancel()
            print 'cancel'