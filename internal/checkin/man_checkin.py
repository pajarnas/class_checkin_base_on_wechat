#encoding=utf-8
from internal.base_file.base_file import BaseFile,DetailFile,SumFile
from checkin import Checkin
from printinfo import PrtInfo
import os,time
class ManCheckin (Checkin):

    def __init__(self,wechat_id):
        Checkin.__init__(self,wechat_id)


    def updateStuDetailCheckinResult(self,stu_id,seq_id):
        detail_records = BaseFile.read_file(self.initDetailName(self.tea_id,self.crs_id,seq_id))
        for detail_rec in detail_records:
            if detail_rec['StuID'] == str(stu_id):
                if detail_rec['checkinResult'] == '请假提交':
                    if raw_input(PrtInfo.promptMessage(4)) == 'y' | 'Y':
                        detail_rec['checkinResult'] = '请假'
                    else:
                        detail_rec['checkinResult'] = '缺勤'
                detail_rec['checkinResult'] = raw_input(PrtInfo.promptMessage(4))
                print PrtInfo.successMessage(0)+detail_rec['checkinResult']
                detail_file = DetailFile(self.initDetailName(self.tea_id,self.crs_id,self.seq_id))
                detail_file.write_file(detail_records)
                return True
        print PrtInfo.notFoundMessage(3)
        return False



    def initDetailRecords(self):
        stu_records = BaseFile.read_file(Checkin.student_file.name)
        temp_list = []
        for stu_rec in stu_records:
            temp_dict = {'StuID': stu_rec['StuID'],
                         'checkinTime': time.strftime('%Y-%m-%d %H:%M:%S'),
                         'ProofPath': None,
                         'checkinType': 'Man',
                         'IsSuc': None,
                         'checkinResult': '出勤'
                         }
            temp_list.append(temp_dict)
        print PrtInfo.successMessage(3)
        return temp_list

if __name__ == '__main__':
    # 教师开启手工考勤的用例描述:
    c= ManCheckin('wonka80')#创建对象,完成考勤对象依赖的初始化
    c.addSeqId(c.seq_id) # 在seq文件中保存此次seq id 记录
    c.createDetailFile([])  # 创建空的文件 detail和 sumfile
    # c.updateSum()
    # stu_id = 201416920101
    seq_id = c.seq_id
    # c.updateStuDetailCheckinResult(stu_id,seq_id)
    stu_id = 201416920102
    c.updateStuDetailCheckinResult(stu_id, seq_id)
    c.updateSumByCertaiSeqId(seq_id)



