#encoding=utf-8
import os
import time

import checkin.importcsv.fileimport.import_course
import checkin.importcsv.fileimport.import_student
import checkin.importcsv.fileimport.import_teacher
from checkin.forms.base_form import Form
from checkin.internal.base_file.base_file import BaseFile, SeqFile, SumFile, DetailFile, StudentFile, CourseFile, \
    TeacherFile
from checkin.my_exceptions import NouFoundException
from checkin.printinfo import PrtInfo
from subject_observer import Subject
from forms.base_form import Form
from checkin.internal.checkin_files import ReadIni


class BaseCheckin(Subject):

    checkin_list = []

    seq_file = SeqFile()
    student_file = StudentFile()
    course_file = CourseFile()
    teacher_file = TeacherFile()

    # 当边界类确定系统时间是合法的时候 才能创建自动考勤对象
    def __init__(self, wechat_id):
        Subject.__init__(self)
        self.wechat_id = wechat_id
        self.tea_id = BaseCheckin.init_teacher_id_by_wechatid(wechat_id)
        self.crs_id = BaseCheckin.init_course_id_by_wechatid(wechat_id)
        self.seq_id = BaseCheckin.init_seq_id(self.tea_id, self.crs_id)
        self.init_files()




    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.append(observer)

    def notify(self):
        for obj in self.observers:
            obj.update()

    def init_files(self):
        if not os.path.exists(self.seq_file.name):
            self.seq_file.write_file([])
        if not os.path.exists(self.course_file.name):
            checkin.importcsv.fileimport.import_course.ImportCourseInfo()
        if not os.path.exists(self.student_file.name):
            checkin.importcsv.fileimport.import_student.ImportStudentInfo()
        if not os.path.exists(self.teacher_file.name):
            checkin.importcsv.fileimport.import_teacher.ImportTeacherInfo()

    @staticmethod
    # 某一教师某一次课在目前seq本地数据源文件获取中最新id
    def init_seq_id(tea_id, crs_id):
        seq_records = BaseFile.read_file(BaseCheckin.seq_file.name)
        seq_id = 1
        i = 1
        while os.path.exists(BaseCheckin.init_detail_name(tea_id,crs_id,i)):
            i += 1
        for record in seq_records:
            if (record['TeacherID'] == str(tea_id)) & (record['CourseID'] == str(crs_id)):
                seq_id = int(record['SeqID']) + 1
        if seq_id < i:
            seq_id = i
        return seq_id

    @staticmethod
    # 某一教师某一次课某一次序的考勤详细表名字
    def init_detail_name(tea_id,crs_id,seq_id):
        return ReadIni().read_path()['files_path']+('_'.join([str(tea_id),str(crs_id),str(seq_id)]))+'_checkinDetail.csv'

    @staticmethod
    # 某一教师某一次课所有次序的考勤总表名字
    def init_sum_name(tea_id,crs_id):
        return ReadIni().read_path()['files_path']+str(tea_id)+'_'+str(crs_id)+'_sum.csv'

    @staticmethod
    # 某一微信号在目前teacher_info本地数据源文件对应的教师id
    def init_teacher_id_by_wechatid(wechat_id):
        tea_records = BaseFile.read_file(BaseCheckin.teacher_file.name)
        tea_id = 0
        for record in tea_records:
            if record['WeChatID'] == wechat_id:
                tea_id = record['TeacherID']
        return tea_id


    @staticmethod
    # 通过终端确定某一个教师对应的所有课程号中哪一个
    def init_course_id_by_wechatid(wechat_id):
        tea_id = BaseCheckin.init_teacher_id_by_wechatid(wechat_id)
        crs_id_list = []
        crs_records = BaseFile.read_file(BaseCheckin.course_file.name)
        for record in crs_records:
            if (record['TeacherID'] == tea_id) & (record['CourseID'] not in crs_id_list):
                crs_id_list.append(record['CourseID'])
        if crs_id_list == []:
            print PrtInfo.notFoundMessage(1)
            return 0
        while True:
            crs_id_list.append('back')
            f = Form(['Course ID'],crs_id_list)
            c = f.init_form()
            if c == len(crs_id_list):
                return 0
            else:
                return f.items[c-1]

    @staticmethod
    # 通过学生微信号判断并找到要参加的考勤对象
    def find_checkin_obj_with_wechat_id(wechat_id):
        if BaseCheckin.checkin_list == []:
            print PrtInfo.failedMessage(0)
            return None
        else:
            print PrtInfo.promptMessage(10)
            tea_ids = []
            for i in BaseCheckin.checkin_list:
                tea_ids.append(i.tea_id)
            choice = Form(['teacher id'],tea_ids).init_form()
            if choice == -1:
                return None
            tea_id = tea_ids[choice - 1]
            for i in BaseCheckin.checkin_list:
                if i.tea_id == tea_id:
                    if i.get_stu_id_in_class_list(wechat_id) != None:
                        return i
                    else:
                        print PrtInfo.notFoundMessage(4)
                        return None
            else:
                print PrtInfo.failedMessage(0)
                return None

    @staticmethod
    # 通过学生微信号判断并找到要参加的考勤对象
    def find_checkin_obj_for_tea(wechat_id):
        if BaseCheckin.checkin_list == []:
            print PrtInfo.failedMessage(6)
            return None
        else:
            tea_id = BaseCheckin.init_teacher_id_by_wechatid(wechat_id)
            for i in BaseCheckin.checkin_list:
                if i.tea_id == tea_id:
                        return i
            else:
                print PrtInfo.failedMessage(6)
                return None

    # 获取从文件中该考勤对象的所有学生
    def init_student_records(self):
        stu_records = BaseFile.read_file(BaseCheckin.student_file.name)
        class_list = self.init_class_records()
        temp_list = []
        for stu_rec in stu_records:
            if stu_rec['ClassID'] in class_list:
                temp_list.append(stu_rec)
        print PrtInfo.successMessage(1)
        return temp_list

    # 获取从文件中该考勤对象的某学生的name
    def get_student_name(self,id):
        stu_records = self.init_student_records()
        for i in stu_records:
            if i['StuID'] == id:
                 return i['StuName']

    # 将本次考勤次序号保存写入文件
    def add_seq_id(self, seq_id):
        seq_rec = {'TeacherID':self.tea_id,
                            'CourseID':self.crs_id,
                            'SeqID':str(int(seq_id)),
                            'Time':time.strftime('%Y-%m-%d %H:%M:%S')
                            }
        self.seq_file.write_file(data=[dict(seq_rec)], way='ab')

    def init_class_records(self):
            crs_list = CourseFile.read_file(BaseCheckin.course_file.name)
            class_list = []
            for crs_rec in crs_list:
                if (crs_rec['TeacherID'] == str(self.tea_id)) & (crs_rec['CourseID'] == str(self.crs_id)):
                    class_list.append(crs_rec['ClassNums'])
            return class_list

    @staticmethod
    # 筛去混乱的detail文件中无效的数据
    def filter_invalid_detail_records(detail_records):
        id_list = []
        for stu in detail_records:
            if stu['StuID']:
                id_list.append(stu['StuID'])
        id_list = list(set(id_list))
        temp_list = []
        detail_records.reverse()
        for id_line in id_list:
            for rec in detail_records:
                if rec['StuID'] == id_line:
                    temp_list.append(rec)
                    break
        return temp_list

    # 大更新 不需要参数 自动完成所有相关detail的更新
    def update_sum(self):
        seq_id = self.init_seq_id(self.tea_id,self.crs_id)
        sum_records = [] # 保存sum文件中所有记录
        for stu_rec in self.init_student_records(): # 获取本班所有学生的记录
            sum_rec_dict = {'StuID': stu_rec['StuID']} # 遍历学生记录列表
            for i in range(1, int(seq_id)):# 将每一个学生在sum文件中都以{'StuID':'11222,'checkin1':'缺勤',....}形式保存
                sum_rec_dict.update({'checkin' + str(i): 'None'}) # seq id 代表次序号,第1,2,3,4...次考勤
            sum_records.append(sum_rec_dict)
        for i in range(1, int(seq_id) ):
            detail_records = BaseFile.read_file(self.init_detail_name(self.tea_id,self.crs_id,i))
            detail_records = self.filter_invalid_detail_records(detail_records) # 读取每一次考勤记录的文件
            for detail_rec in detail_records:
                for sum_rec in sum_records:
                    if sum_rec['StuID'] == detail_rec['StuID']:
                        sum_rec['checkin' + str(i)] = detail_rec['checkinResult']
        sum_file = SumFile(self.init_sum_name(self.tea_id, self.crs_id))
        sum_file.columns = ['StuID']
        for i in range(1, int(seq_id)):
            sum_file.columns.append('checkin' + str(i))
        sum_file.write_file(sum_records)

    # 小更新 只会更新其中一列, 更新哪一列 需要指定seq_id
    # 完成后, 小更新一次.只更新最新的次序号,
    # 先生成考勤结果列表, 从detail文件中读取, 最后一次的,
    # 考勤结果, 与学号, 写入文件中, 最终生成一个列表, 然后将列表传入小更新函数
    # 小更新([{考勤结果, 考勤学生学号}], 次序号), 遍历文件, 如果学号和列表中的某一个相同,
    # 更新.捕获异常, 文件遍历完却在列表中找不到该学生, 和学号中存在
    # 但是文件中不存在的异常

    # 根据seq_id更新sum文件中某一列数据
    def update_sum_by_certain_seq_id(self, seq_id):
        if not os.path.exists(self.init_sum_name(self.tea_id,self.crs_id)) :
            self.update_sum()
            return
        result_records = []
        detail_records = BaseFile.read_file(self.init_detail_name(self.tea_id, self.crs_id,seq_id))
        detail_records = self.filter_invalid_detail_records(detail_records)
        for rec in detail_records:
            temp_dict = {'StuID': rec['StuID'], 'checkin'+str(seq_id): rec['checkinResult']}
            result_records.append(temp_dict)
        sum_records = SumFile.read_file(self.init_sum_name(self.tea_id,self.crs_id))
        for s_rec in sum_records:
            for r_rec in result_records:
                if s_rec['StuID'] == r_rec['StuID']:
                    s_rec.update(r_rec)
        sum_file = SumFile(self.init_sum_name(self.tea_id, self.crs_id))
        sum_file.columns = ['StuID']
        for i in range(1, int(self.seq_id) + 1):
            sum_file.columns.append('checkin' + str(i))
        sum_file.write_file(sum_records)

    def write_detail_file(self, detail_records):
        DetailFile(self.init_detail_name(self.tea_id, self.crs_id, self.seq_id)).write_file(detail_records)
        print PrtInfo.successMessage(4)



if __name__ == '__main__':
    l = BaseCheckin.course_file.read_file(BaseCheckin.course_file.name)
    print l
