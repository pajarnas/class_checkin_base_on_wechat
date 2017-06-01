#encoding=utf-8

import csv
import os

from internal.checkin import checkin


class ManCheckin(checkin.Checkin):
    # 手工考勤控制类的初始化
    def __init__(self,wechat_id,course_id):
        checkin.CheckinCtrl.__init__(self, wechat_id, course_id)

    # 教师进行手工考勤修改
    def setDetailFile(self):
        fileName = self.getDetailName()
        stu_id = raw_input('输入你想要修改的学生学号')
        check_result = raw_input('输入该学生的考勤结果：')

        with open(fileName, 'r+') as changeName:
            list_lines = changeName.readlines()
            d = ''
            for str_line in list_lines:
                list_line = str_line.split(',')
                if list_line[0] == stu_id:
                    list_line[5] = check_result
                    d += ','.join(list_line) + '\n'
                else:
                    d += str_line
            changeName.seek(0)  # 从文件头还始
            changeName.truncate()  # 清空文件
            changeName.write(d)  # 将修改后的内容写入
        print '您已成功修改该学生的考勤结果'

    #教师进行手工考勤增加
    def getDetailFile(self):
        teacher_id = self.findTeacheridByWechatid()
        self.setSeqFile()
        detail_name = 'internal/' + str(teacher_id) + '_' + str(self.course_id) + '_' + \
                   str(self.seq_id) + '_' + 'checkinDetail.csv'
        with open(detail_name, 'ab+') as  detail_file:
            writer = csv.writer(detail_file)
            message0 = ['StuID', 'checkinTime', 'ProofPath', 'checkinType', 'IsSuss', 'checkinResult']
            writer.writerow(message0)
            sum_name = 'internal/' + teacher_id + '_' + str(self.course_id) + '_' + 'sum.csv'
            self.getSumFile()
            with open(sum_name, 'r') as sum_file:
                sum_reader = csv.reader(sum_file)
                sum_reader.next()
                for line in sum_reader:  #从sum文件里找到学生的id
                    message = [line[0], '无', '无', 'man', 'True', '出勤']
                    writer.writerow(message)
        print '您已成功增加一次考勤记录，并以默认所有学生出勤'

    #重写getsum 因为手工考勤是不需要进入s全局队列中去的
    def getSumFile(self):
        teacher_id = self.findTeacheridByWechatid()
        sum_name = 'internal/' + str(teacher_id) + '_' + str(self.course_id) + '_' + "sum.csv"
        if os.path.exists(sum_name) != True:
            with open(sum_name, 'ab+') as sum_file:
                sum_writer = csv.writer(sum_file)
                string_to_add = ['StuID', '']
                sum_writer.writerow(string_to_add)
                class_list = []
                with open('internal/courseInfo.csv', 'rb') as courseInfo:
                        class_reader = csv.reader(courseInfo)
                        class_reader.next()
                        for class_line in class_reader:
                            if (class_line[2] ==  str(teacher_id)) & (class_line[0] == str(self.course_id)):
                                class_list.append(class_line[3])

                with open('internal/studentInfo.csv', 'rb') as studentInfo:
                        stu_reader = csv.reader(studentInfo)
                        stu_reader.next()
                        for stu_line in stu_reader:
                            if stu_line[2] in class_list:
                                str_stu = [stu_line[0], '']
                                sum_writer.writerow(str_stu)


#教师所能进行的手工考勤
if __name__ == "__main__":
    t = ManCheckinCtrl("wonka80", 51610134)
    t.getDetailFile()
    t.setDetailFile()
    pass