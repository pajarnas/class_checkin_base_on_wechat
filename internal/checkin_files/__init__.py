#coding=utf-8
import ConfigParser
import re
import os

# 读取配置文件信息   节次信息    返回一个节次开始和结束时间的列表
l = (os.path.dirname(os.path.realpath(__file__)).split('/'))
l.pop(-1)
l.pop(-1)
l.append('')
base = '/'.join(l)


class ReadIni():

    begin_time_list = [] # 设置一个列表存两节课的开始和结束时间


    def __init__(self):
        self.begin_time_list = self.read_begin(self.begin_time_list)

    def read_begin(self,class_time_list ):
        cf = ConfigParser.ConfigParser()
        cf.read(base+'internal/settings.ini')

        time = re.split('-|:', cf.get('sectime', 'sec1'))
        time_dict = {'StartTime': str(time[0])+':' + str(time[1]),
                     'EndTime': str(time[2])+':' + str(time[3]) }
        class_time_list.append(time_dict)

        time = re.split('-|:', cf.get('sectime', 'sec2'))
        time_dict = {'StartTime': str(time[0])+':' + str(time[1]),
                     'EndTime': str(time[2]) +':'+ str(time[3]) }
        class_time_list.append(time_dict)
        # 第三四节课的时间始末
        time = re.split('-|:', cf.get('sectime', 'sec3'))
        time_dict = {'StartTime': str(time[0]) +':'+ str(time[1]),
                     'EndTime': str(time[2])+':' + str(time[3])}
        class_time_list.append(time_dict)
        time = re.split('-|:', cf.get('sectime', 'sec4'))
        time_dict = {'StartTime': str(time[0])+':' + str(time[1]),
                     'EndTime': str(time[2])+':' + str(time[3])}
        class_time_list.append(time_dict)
        # 第四五节课的时间始末
        time = re.split('-|:', cf.get('sectime', 'sec5'))
        time_dict = {'StartTime': str(time[0])+':' + str(time[1]),
                     'EndTime': str(time[2])+':' + str(time[3])}
        class_time_list.append(time_dict)
        # 第四五节课的时间始末
        time = re.split('-|:', cf.get('sectime', 'sec6'))
        time_dict = {'StartTime': str(time[0]) + ':' + str(time[1]),
                     'EndTime': str(time[2]) + ':' + str(time[3])}
        class_time_list.append(time_dict)

        time = re.split('-|:', cf.get('sectime', 'sec7'))
        time_dict = {'StartTime': str(time[0]) + ':' + str(time[1]),
                     'EndTime': str(time[2]) + ':' + str(time[3])}
        class_time_list.append(time_dict)

        time = re.split('-|:', cf.get('sectime', 'sec8'))
        time_dict = {'StartTime': str(time[0]) + ':' + str(time[1]),
                     'EndTime': str(time[2]) + ':' + str(time[3])}
        class_time_list.append(time_dict)
        return class_time_list

    def read_late_dev(self,):
        cf = ConfigParser.ConfigParser()
        cf.read(base+'internal/settings.ini')
        return int(cf.get('latedev', 'latedev'))

    @staticmethod
    def read_path():
        cf = ConfigParser.ConfigParser()
        cf.read(base+'internal/settings.ini')
        dic = {}
        dic.update({'tea_path':base+cf.get('path', 'tea_path')})
        dic.update({'crs_path': base+cf.get('path', 'crs_path')})
        dic.update({'seq_path': base+cf.get('path', 'seq_path')})
        dic.update({'files_path': base+cf.get('path', 'files_path')})
        dic.update({'stu_path': base+cf.get('path', 'stu_path')})
        return dic

if __name__ == '__main__':
    t = ReadIni()
    nowtime = '02:15'
    nowtime = int(''.join(nowtime.split(':')))
    for i in range(0, 8):
        e = int(''.join(t.begin_time_list[i]['EndTime'].split(':')))
        s = int(''.join(t.begin_time_list[i]['StartTime'].split(':')))
        print e
        print s
        if (nowtime >= s) & (nowtime <= e):
            print i + 1
    else:
        print 0