#encoding=utf-8
from checkin.internal.base_file.base_file import BaseFile,DetailFile,SumFile
from base_checkin import BaseCheckin
from checkin.printinfo import PrtInfo
import os,time


class ManCheckin (BaseCheckin):

    def __init__(self, wechat_id):
        BaseCheckin.__init__(self,wechat_id)

    @staticmethod
    def update_stu_detail_checkin_result(stu_id, seq_id,tea_id,crs_id):
        detail_records = BaseFile.read_file(BaseCheckin.init_detail_name(tea_id,crs_id, seq_id))
        for detail_rec in detail_records:
            if detail_rec['StuID'] == str(stu_id):
                if detail_rec['checkinResult'] == '请假提交':
                    if raw_input(PrtInfo.promptMessage(4)) == 'y' | 'Y':
                        detail_rec['checkinResult'] = '请假'
                    else:
                        detail_rec['checkinResult'] = '缺勤'
                detail_rec['IsSuc'] = 'True'
                detail_rec['checkinResult'] = raw_input(PrtInfo.promptMessage(4))
                print PrtInfo.successMessage(0)+detail_rec['checkinResult']
                detail_file = DetailFile(BaseCheckin.init_detail_name(tea_id, crs_id, seq_id))
                detail_file.write_file([detail_rec],'ab')
                return True
        print PrtInfo.notFoundMessage(3)
        return False

    @staticmethod
    def confirm_leave(obj,detail_file):
        records = BaseFile.read_file(detail_file.name)
        leave_list = []
        for rec in records:
            if rec['checkinResult'] == '假条提交':
                leave_list.append(rec)
        if leave_list is not []:
            print 'You have ' + str(leave_list.__len__()) + ' leave events to handle!'
            for line in leave_list:
                print 'Name:' + BaseCheckin.get_student_name(obj,line['StuID'])
                print 'Image:' + line['ProofPath']
                choice = raw_input(PrtInfo.promptMessage(8))
                if choice == 'y':
                    print line['ProofPath']
                    line['checkinResult'] = '请假'
                else:
                    print line['ProofPath']
                    line['checkinResult'] = '缺勤'
                detail_file.write_file([line], 'ab')

    def init_detail_records(self):
        stu_records = BaseFile.read_file(BaseCheckin.student_file.name)
        temp_list = []
        for stu_rec in stu_records:
            temp_dict = {'StuID': stu_rec['StuID'],
                         'checkinTime': time.strftime('%Y-%m-%d %H:%M:%S'),
                         'ProofPath': 'Auto',
                         'checkinType': 'Man',
                         'IsSuc': 'True',
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



