#encoding=utf-8
from abc import ABCMeta, abstractmethod
from internal.base_file.base_file import BaseFile,SeqFile,SumFile,DetailFile,StudentFile,CourseFile,TeacherFile
from printinfo import PrtInfo
import time,os




class Checkin():

    checkin_list = []

    seq_file = SeqFile('../seq.csv')
    student_file = StudentFile('../studentInfo.csv')
    coures_file = CourseFile('../courseInfo.csv')
    teacher_file = TeacherFile('../teacherInfo.csv')

    # 当边界类确定系统时间是合法的时候 才能创建自动考勤对象
    def __init__(self,wechat_id):
        self.wechat_id = wechat_id
        self.tea_id = Checkin.initTeacherIdByWechatid(wechat_id)
        self.crs_id = Checkin.initCourseIdByWechatid(wechat_id)
        self.seq_id = Checkin.initSeqId(self.tea_id, self.crs_id)

    @staticmethod
    # 某一教师某一次课在目前seq本地数据源文件获取中最新id
    def initSeqId(tea_id, crs_id):
        seq_records = BaseFile.read_file(Checkin.seq_file.name)
        seq_id = 1
        for record in seq_records:
            if (record['TeacherID'] == str(tea_id)) & (record['CourseID'] == str(crs_id)):
                seq_id = int(record['SeqID']) + 1
        return seq_id

    @staticmethod
    # 某一教师某一次课某一次序的考勤详细表名字
    def initDetailName(tea_id,crs_id,seq_id):
        return '_'.join([str(tea_id),str(crs_id),str(seq_id)])+'_checkinDetail.csv'

    @staticmethod
    # 某一教师某一次课所有次序的考勤总表名字
    def initSumName(tea_id,crs_id):
        return str(tea_id)+'_'+str(crs_id)+'_sum.csv'

    @staticmethod
    # 某一微信号在目前teacher_info本地数据源文件对应的教师id
    def initTeacherIdByWechatid(wechat_id):
        tea_records = BaseFile.read_file(Checkin.teacher_file.name)
        tea_id = 0
        for record in tea_records:
            if (record['WeChatID'] == wechat_id):
                tea_id = record['TeacherID']
        return tea_id

    @staticmethod
    # 通过终端确定某一个教师对应的所有课程号中哪一个
    def initCourseIdByWechatid(wechat_id):
        tea_id = Checkin.initTeacherIdByWechatid(wechat_id)
        crs_id_list = []
        crs_records = BaseFile.read_file(Checkin.coures_file.name)
        for record in crs_records:
            if (record['TeacherID'] == tea_id) & (record['CourseID'] not in crs_id_list):
                crs_id_list.append(record['CourseID'])
        if crs_id_list == []:
            print PrtInfo.notFoundMessage(1)
            return 0
        while True:
            print PrtInfo.promptMessage(2)
            print crs_id_list
            crs_id = raw_input(PrtInfo.promptMessage(1))
            if crs_id not in crs_id_list:
                print PrtInfo.notFoundMessage(2)
            else:
                return crs_id

    def initSumRecords(self):
        temp_list = []
        if os.path.exists(self.sum_file.name):
            sum_records = BaseFile.read_file(self.sum_file.name)
            for sum_rec in sum_records:
                    temp_list.append(sum_rec)
            print PrtInfo.successMessage(2)
            return temp_list
        else:
            temp_dict = {}
            for stu_rec in self.student_records:
                temp_dict['StuID'] = stu_rec['StuID']
                temp_list.append(temp_dict)
            print PrtInfo.successMessage(2)
            return temp_dict

    @abstractmethod
    def initDetailRecords(self):
        return []

    def initStudentRecords(self):
        stu_records = BaseFile.read_file(Checkin.student_file.name)
        csr_records = BaseFile.read_file(Checkin.coures_file.name)
        class_list = []
        for crs_rec in csr_records:
            if (crs_rec['TeacherID'] == str(self.tea_id)) & (crs_rec['CourseID'] == str(self.crs_id)):
                class_list.append(crs_rec['ClassNums'])
        temp_list = []
        for stu_rec in stu_records:
            if stu_rec['ClassID'] in class_list:
                temp_list.append(stu_rec)
        print PrtInfo.successMessage(1)
        return temp_list

    def insertNewSeqRecord(self):
        seq_records = self.seq_file.read_file(self.seq_file.name)
        seq_records.append({'TeacherID':self.tea_id,
                            'CourseID':self.crs_id,
                            'SeqID':str(int(self.seq_id)),
                            'Time':time.strftime('%Y-%m-%d %H:%M:%S')
                            })
        self.seq_file.write_file(seq_records)

    def initSumFile(self):
        sum_file = SumFile(self.initSumName())
        sum_file.columns = ['StuID']
        for i in range(1, int(self.seq_id) + 1):
            sum_file.columns.append('checkin' + str(i))
        return sum_file

    def insertSumRecord(self,sum_records,detail_records,checkin_id):
        for detail_rec in detail_records:
            for sum_rec in sum_records:
                if sum_rec['StuID'] == detail_rec['StuID']:
                    sum_rec['checkin'+str(checkin_id)] = detail_rec['checkinResult']

    def updateSum(self):
        self.sum_records = []
        for stu_rec in self.student_records:
            sum_rec_dict = {'StuID':stu_rec['StuID']}
            self.sum_file.columns = ['StuID']
            for i in range(1, int(self.seq_id) + 1):
                sum_rec_dict.update({'checkin'+str(i):'None'})
                self.sum_file.columns.append('checkin'+str(i))
            self.sum_records.append(sum_rec_dict)
        for i in range(1,int(self.seq_id) + 1):
            detail_list = BaseFile.read_file('_'.join([str(self.tea_id),str(self.crs_id),str(i)])+'_checkinDetail.csv')
            self.insertSumRecord(self.sum_records,detail_list,i)

    def createDetailFiles(self):
        self.detail_file.write_file(self.detail_records)
        print PrtInfo.successMessage(4)

    def createSumFiles(self):
        self.updateSum()
        self.sum_file.write_file(self.sum_records)