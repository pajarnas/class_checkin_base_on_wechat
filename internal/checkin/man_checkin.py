#encoding=utf-8
from internal.base_file.base_file import BaseFile,DetailFile,SumFile
from checkin import Checkin
from printinfo import PrtInfo
import os,time
class ManCheckin (Checkin):

    def __init__(self,wechat_id):
        Checkin.__init__(self,wechat_id)
        self.detail_records = self.initDetailRecords()

    def updateDetailRecords(self):
        stu_id = raw_input(PrtInfo.promptMessage(3))
        check_result = raw_input(PrtInfo.promptMessage(4))
        flag = 0
        for detail_rec in self.detail_records:
            if detail_rec['StuID'] == stu_id:
                flag = 1
                detail_rec['checkinResult'] = check_result
        if flag == 1 :
            detail_file = DetailFile(self.detail_file.name)
            detail_file.write_file(self.detail_records)
            print PrtInfo.successMessage(5)
        else:
            print PrtInfo.notFoundMessage(3)

    def initDetailRecords(self):
        stu_records = BaseFile.read_file(Checkin.student_file.name)
        temp_list = []
        for stu_rec in stu_records:
               
                temp_list.append(temp_dict)
        print PrtInfo.successMessage(3)
        return temp_list

if __name__ == '__main__':
    c= ManCheckin('wonka80')#创建对象,完成考勤对象依赖的初始化
    c.insertNewSeqRecord()
    c.createLocalFiles()  # 创建空的文件 detail和sumfile


