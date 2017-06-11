import time,threading


def p():
    print type(i)

l = threading.Timer(5,p)
l.start()
li = []
li.append(l)
time.sleep(1)
l.cancel()
l2 = threading.Timer(5,p)
l2.start()
li.append(l2)
for i in li:
    if i.isAlive():
        print 'wo cao'