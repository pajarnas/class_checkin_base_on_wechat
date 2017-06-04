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

    # 增加seq记录到seq file 文件
    def addSeqId(self,seq_id):
        seq_rec = {'TeacherID':self.tea_id,
                            'CourseID':self.crs_id,
                            'SeqID':str(int(seq_id)),
                            'Time':time.strftime('%Y-%m-%d %H:%M:%S')
                            }
        self.seq_file.write_file(data=[dict(seq_rec)],way='ab')

    # 初始化当前的考勤的 Sum 文件
    # def initSumFile(self):
    #     sum_file = SumFile(self.sum_name)
    #     sum_file.columns = ['StuID']
    #     for i in range(1, int(self.seq_id) + 1):
    #         sum_file.columns.append('checkin' + str(i))
    #     return sum_file

    def initSumFile(self):
        sum_file = SumFile(self.initSumName(self.tea_id,self.crs_id))
        sum_file.columns = ['StuID']
        for i in range(1, int(self.seq_id) + 1):
            sum_file.columns.append('checkin' + str(i))
        return sum_file

    # 大更新 不需要参数 自动完成所有相关detail的更新
    def updateSum(self):
        if not self.isSumExist():
            return
        sum_records = []
        for stu_rec in self.initStudentRecords():
            sum_rec_dict = {'StuID': stu_rec['StuID']}
            for i in range(1, int(self.seq_id) + 1):
                sum_rec_dict.update({'checkin' + str(i): 'None'})
            sum_records.append(sum_rec_dict)
        for i in range(1, int(self.seq_id) + 1):
            detail_records = BaseFile.read_file(self.initDetailName(self.tea_id,self.crs_id,self.seq_id))
            for detail_rec in detail_records:
                for sum_rec in sum_records:
                    if sum_rec['StuID'] == detail_rec['StuID']:
                        sum_rec['checkin' + str(i)] = detail_rec['checkinResult']
        self.initSumFile().write_file(sum_records)

    # 小更新 只会更新其中一列, 更新哪一列 需要指定seq_id
    # 完成后, 小更新一次.只更新最新的次序号,
    # 先生成考勤结果列表, 从detail文件中读取, 最后一次的,
    # 考勤结果, 与学号, 写入文件中, 最终生成一个列表, 然后将列表传入小更新函数
    # 小更新([{考勤结果, 考勤学生学号}], 次序号), 遍历文件, 如果学号和列表中的某一个相同,
    # 更新.捕获异常, 文件遍历完却在列表中找不到该学生, 和学号中存在
    # 但是文件中不存在的异常
    def isSumExist(self):
        temp_list = []
        if not os.path.exists(self.initSumName(self.tea_id,self.crs_id)):
            temp_dict = {}
            for stu_rec in self.initStudentRecords():
                temp_dict['StuID'] = stu_rec['StuID']
                temp_list.append(temp_dict)
            SumFile(self.initSumName(self.tea_id,self.crs_id)).write_file(temp_list)
            print PrtInfo.successMessage(2)
            return False
        else:
            return True
    def updateSumByCertaiSeqId(self,seq_id):
        if not self.isSumExist():
            return
        result_records = []
        detail_records = BaseFile.read_file(self.initDetailName(self.tea_id,self.crs_id,seq_id))
        for rec in detail_records:
            temp_dict = {'StuID': rec['StuID'], 'checkin'+str(seq_id): rec['checkinResult']}
            result_records.append(temp_dict)
        sum_records = SumFile.read_file(self.initSumName(self.tea_id,self.crs_id))
        for s_rec in sum_records:
            for r_rec in result_records:
                if s_rec['StuID'] == r_rec['StuID']:
                    s_rec.update(r_rec)
        sum_file = self.initSumFile()
        sum_file.write_file(sum_records)

    def createDetailFile(self,detail_records):
        DetailFile(self.initDetailName(self.tea_id,self.crs_id,self.seq_id)).write_file(detail_records)
        print PrtInfo.successMessage(4)