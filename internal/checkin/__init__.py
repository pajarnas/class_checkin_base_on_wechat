#coding=utf-8
import ConfigParser
import re


# 读取配置文件信息   节次信息    返回一个节次开始和结束时间的列表
class ReadIni :

    begin_time_list = [] # 设置一个列表存两节课的开始和结束时间

    def __init__(self):
        self.begin_time_list = self.read_begin(self.begin_time_list)

    def read_begin(self,class_time_list ):
        cf = ConfigParser.ConfigParser()
        cf.read('../settings.ini')

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
        return class_time_list

if __name__ == '__main__':

    def initSectionId(nowtime):
        t = ReadIni()
        nowtime = int(''.join(nowtime.split(':')))
        for i in range(0, 5, 1):
            e = int(''.join(t.class_time_list[i]['EndTime'].split(':')))
            s = int(''.join(t.class_time_list[i]['StartTime'].split(':')))
            if (nowtime >= s) & (nowtime <= e):
                return i + 1
        else:
            return 0
    print initSectionId('10:40')

