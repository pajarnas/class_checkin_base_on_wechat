#encoding=utf-8
from internal.base_file.base_file import BaseFile,DetailFile,SumFile,CourseFile
from base_checkin import BaseCheckin
from subject_observer import Observer
from printinfo import PrtInfo
from my_exceptions import NouFoundException,WrongException
from __init__ import ReadIni
from time_window import Timer
import time
import random


class AutoCheckin(BaseCheckin):

    def __init__(self, wechat_id):
        BaseCheckin.__init__(self, wechat_id)
        self.class_list = self.init_class_list()
        self.enter_time = time.strftime('%H:%M')
        self.section_id = self.init_section_id(time.strftime('%H:%M'))
        self.time_window = Timer()

    def init_class_list(self):
            crs_list = CourseFile.read_file(BaseCheckin.course_file.name)
            class_list = []
            for crs_rec in crs_list:
                if (crs_rec['TeacherID'] == str(self.tea_id)) & (crs_rec['CourseID'] == str(self.crs_id)):
                    class_list.append(crs_rec['ClassNums'])
            if class_list == []:
                raise NouFoundException, PrtInfo.notFoundMessage(5)
            return class_list

    def init_section_id(self, nowtime):
        t = ReadIni()
        nowtime = int(''.join(nowtime.split(':')))
        for i in range(0, 5, 1):
            e = int(''.join(t.begin_time_list[i]['EndTime'].split(':')))
            s = int(''.join(t.begin_time_list[i]['StartTime'].split(':')))
            if (nowtime >= s) & (nowtime <= e):
                return i + 1
        else:
            return 0

    def init_detail_records(self):
        stu_records = self.init_student_records()
        temp_list = []
        for stu_rec in stu_records:
                temp_dict = {'StuID':stu_rec['StuID'],
                             'checkinTime':time.strftime('%Y-%m-%d %H:%M:%S'),
                             'ProofPath':None,
                             'checkinType':'Auto',
                             'IsSuc':None,
                             'checkinResult':'缺勤'
                             }
                temp_list.append(temp_dict)
        print PrtInfo.successMessage(3)
        return temp_list

    def entry_list(self):
        # self.enter_time = '8:30'
        self.section_id = self.init_section_id(self.enter_time)
        class_list = self.init_class_list()
        intersection_flag = False

        # 全局队列为空:
        if BaseCheckin.checkin_list == []:
            # print PrtInfo.successMessage(7)
            BaseCheckin.checkin_list.append(self)
            self.time_window.start_timing(10)
            print 'enter OK,start timing 10 s'
            return True
        # 非空
        kick_head = False
        for checkin_obj in BaseCheckin.checkin_list[:]:
            if set(class_list) & set(checkin_obj.class_list):
                # 存在交集
                # 节次不一样 踢掉
                if self.section_id != checkin_obj.section_id:
                    intersection_flag = True
                    if BaseCheckin.checkin_list.index(checkin_obj) == 0:
                        # 踢掉的是队首
                        kick_head = True
                        # print PrtInfo.successMessage(6)
                    print 'Kick one OK'
                    checkin_obj.notify()
                    BaseCheckin.checkin_list.remove(checkin_obj)
                # 节次一样,无法进入,退出函数
                else:
                    print 'filed to enter OK'
                    return False
                    #raise WrongException, PrtInfo.failedMessage(2)
        # 队列中的所有班都与来者没有交集,或者有交集被踢出去
        if (intersection_flag is False) | (kick_head is False):
            # 没有交集 或者 踢掉的不是队首
            #  print PrtInfo.successMessage(7)
            self.time_window.just_waiting()
            BaseCheckin.checkin_list.append(self)
            print 'just wait OK,enter OK'
        elif (intersection_flag is True) & (kick_head is True) & \
                (BaseCheckin.checkin_list.__len__() is not 0):
            # 有交集 且 踢掉的是队首 且 当前者不是队首
            print PrtInfo.successMessage(7)
            BaseCheckin.checkin_list.append(self)
            t2 = BaseCheckin.checkin_list[0].enter_time
            t3 = BaseCheckin.checkin_list[1].enter_time
            self.time_window.time_second(t2, t3)
            print 'to time second ,third kicked ,time (t2 - t3 )'
        else:
            # 有交集 且 踢掉队首 且 自己是队首
            print PrtInfo.successMessage(7)
            BaseCheckin.checkin_list.append(self)
            print 'become head ,time 100 min'
            self.time_window.start_timing(10)

    def get_stu_id_in_class_list(self, wechat_id):
        student_records = self.init_student_records()
        for stu_rec in student_records:
            if stu_rec['WeChatID'] == wechat_id:
                return stu_rec['StuID']
        else:
            raise NouFoundException,PrtInfo.notFoundMessage(3)

    def upload_path(self):
        return raw_input(PrtInfo.promptMessage(5))


    def judge_result(self,proof_path):
        # isLate(time)
        # isHere(path)
        # isYourself(path)
        i = random.randrange(0, 2)
        if i is 0:
            return 'True'
        if i is 1:
            return 'False'

    def get_detail_record(self, checkin_type, stu_id):
        checkin_result = None
        if raw_input("enter 'y' to ask for leave") is 'y':
            checkin_result = '假条提交'
        proof = self.upload_path()
        judge_result = self.judge_result(proof)
        if judge_result is not True and checkin_result is None:
            print "you are not 'here' or you are not 'you'"
        stu_id = raw_input("enter your student id")
        return {'StuID': stu_id,
                'checkinTime': time.strftime('%Y-%m-%d %H:%M:%S'),
                'ProofPath': proof,
                'checkinType': checkin_type,
                'IsSuc': judge_result,
                'checkinResult': checkin_result}

    def get_latest_record(self, stu_id, checkin_type):
        detail_rec = {}
        detail_records = BaseFile.read_file(self.init_detail_name(self.tea_id,self.crs_id,self.seq_id))
        for rec in detail_records:
            if (rec['StuID'] is str(stu_id)) & (rec['checkinType'] is str(checkin_type)):
                detail_rec = rec
        return detail_rec

    def init_new_detail_record(self, wechat_id, checkin_type):
        # 先判断最新记录是否是True
        stu_id = self.get_stu_id_in_class_list(wechat_id)
        rec = self.get_latest_record(stu_id,checkin_type)
        if rec == {}:
            DetailFile(self.init_detail_name(self.tea_id, self.crs_id, self.seq_id)). \
                write_file([self.get_detail_record(checkin_type, stu_id)], 'ab')
            return
        elif rec['IsSuc'] is not 'True':
            DetailFile(self.init_detail_name(self.tea_id, self.crs_id, self.seq_id)). \
                write_file([self.get_detail_record(checkin_type, stu_id)], 'ab')
            return
        else:
            return

    def start_checkin(self):
        self.attach(EndcheckinObserver(self))
        self.attach(TimeWindowObserver(self))
        if self.entry_list() is not False:
            self.write_detail_file([])
            self.update_sum_by_certain_seq_id(self.seq_id)
            self.add_seq_id(self.seq_id)  # 在seq文件中保存此次seq id 记录

    def join_checkin(self, wechat_id):
        if self in BaseCheckin.checkin_list:
            checkin_type = 'Auto'
            # checkin_type = raw_input(PrtInfo.promptMessage(6))
            if checkin_type == 'Auto':
                self.init_new_detail_record(wechat_id,'Auto')
                PrtInfo.successMessage(8)
                return True
            elif checkin_type == 'Random':
                if self.get_stu_id_in_class_list(wechat_id) not in self.get_random_list():
                    print PrtInfo.notFoundMessage(4)
                    return False
                else:
                    self.init_new_detail_record(wechat_id,'Random')
                    PrtInfo.successMessage(8)
            else:
                print PrtInfo.failedMessage(1)
        else:
            print PrtInfo.failedMessage(0)
            return False

    def get_random_list(self):
        records = BaseFile.read_file(self.init_detail_name(self.tea_id, self.crs_id, self.seq_id))
        random_list = []
        for rec in records:
            if rec['checkinType'] is 'Random' and rec['checkinResult'] is 'init':
                random_list.append(rec['StuID'])

    def start_random_checkin(self,num):
        student_records = self.init_student_records()
        temp_list = random.sample(student_records, num)
        for line in student_records:
            if line in temp_list:
                temp_dict = {'StuID': line['StuID'],
                             'checkinTime': time.strftime('%Y-%m-%d %H:%M:%S'),
                             'ProofPath': 'none',
                             'checkinType': 'Random',
                             'IsSuc':'none' ,
                             'checkinResult': 'init'
                             }
                DetailFile(self.init_detail_name(self.tea_id,self.crs_id,self.seq_id)).write_file([temp_dict],'ab')

    def is_late(self, rec):
        checkin_hr, checkin_min, s = ((rec['checkinTime'].split(' '))[1].split(':'))
        enter_hr,enter_min = self.enter_time.split(':')

        if int(self.section_id) - 1 < 0:
            return '出勤'
        begin_hr, begin_min = ReadIni().begin_time_list[self.section_id - 1]['StartTime'].split(':')
        if int(begin_hr) - int(enter_hr) * 60 + int(begin_min) - int(enter_min) > 0:
            if(int(begin_hr) - int(checkin_hr) )* 60 + (int(begin_min) - int(checkin_min)) < 0:
                return '迟到'
            else:
                return '出勤'
        else:
            if(int(enter_hr) - int(checkin_hr)) * 60 + (int(enter_min) - int(checkin_min)) > 300:
                return '迟到'
            else:
                return '出勤'

    def exit_checkin(self):
        pass


class EndcheckinObserver(Observer):
    def __init__(self,checkin_obj):
        Observer.__init__(self)
        self.checkin_obj = checkin_obj

    def update(self):
        print 'i update'
        # detail_file = DetailFile(self.checkin_obj.initDetailName(self.checkin_obj.tea_id, self.checkin_obj.crs_id, self.checkin_obj.seq_id))
        # for stu in self.checkin_obj.initStudentRecords():
        #     rec = self.checkin_obj.getLatestRecord(stu['StuID'],'Auto')
        #     # 没有签到的学生 缺勤 追加到文件中
        #     if rec == {}:
        #         rec = {'StuID': stu['StuID'],
        #                'checkinTime': time.strftime('%Y-%m-%d %H:%M:%S'),
        #                'ProofPath': 'none',
        #                'checkinType': 'Auto',
        #                'IsSuc': 'none',
        #                'checkinResult': '缺勤'}
        #         detail_file.write_file([rec], 'ab')
        #         continue
        #
        #     # 签到 并且来的学生 检查是否请假
        #     if rec['checkinResult'] == '假条提交':
        #         rec.update({'checkinResult': '假条提交'})
        #         detail_file.write_file([rec], 'ab')
        #         continue
        #
        #     # 签到 并且来的学生 检查是否 迟到
        #     if rec['IsSuc'] == 'True':
        #         rec2 = self.checkin_obj.getLatestRecord(rec['StuID'],'Random')
        #         if rec2 is not {} :
        #             if rec2['IsSuc'] is not 'True':
        #                 rec.update({'checkinResult': '早退'})
        #                 detail_file.write_file([rec], 'ab')
        #                 continue
        #         rec.update({'checkinResult': self.checkin_obj.isLate(rec)})
        #         detail_file.write_file([rec], 'ab')
        #         continue
        #
        #     # 签到失败 没来的学生 记录为缺勤或者早退
        #     if rec['IsSuc'] == 'False':
        #         rec2 = self.checkin_obj.getLatestRecord(rec['StuID'], 'Random')
        #         if rec2 is not {}:
        #             if rec2['IsSuc'] is 'True':
        #                 rec.update({'checkinResult': '迟到'})
        #                 detail_file.write_file([rec], 'ab')
        #                 continue
        #         rec.update({'checkinResult': '缺勤'})
        #         detail_file.write_file([rec], 'ab')
        #         continue
        # Mancheckin.confirmLeave(detail_file)
        # self.checkin_obj.updateSum()


class TimeWindowObserver(Observer):
    def __init__(self,checkin_obj):
        Observer.__init__(self)
        self.checkin_obj = checkin_obj

    def update(self):
        # 问自己是不是队首
        print 'checkin obj cancle threading'
        if self.checkin_obj is BaseCheckin.checkin_list[0]:
            if self.checkin_obj.time_window.t is not None:
                self.checkin_obj.time_window.t.cancel()

if __name__ == '__main__':
    # print checkin.checkin_list
    # c = Autocheckin('w_101')
    # c.entryList()
    # print 'c.section_id:'+ str(c.section_id)
    # print 'c.enter_time:'+str(c.enter_time)

    # 2
    # c = Autocheckin('w_101')
    # c.enter_time = '8:30'
    # c.section_id = 1
    # checkin.checkin_list.append(c)
    # d = Autocheckin('w_102')
    # c.enter_time = '8:40'
    # c.entryList()

    # 3
    # 101 第1节课正在考勤201,第2节课,103考勤203(踢掉队首的代码)

    #
    # c = Autocheckin('w_101')
    # c.enter_time = '8:30'
    # c.section_id = 1
    # checkin.checkin_list.append(c)
    # d = Autocheckin('w_102')
    # d.enter_time = '10:40'
    # d.entryList()

    # 场景4:101
    # 第1节课正在考勤201, 第1节课, 102
    # 正在考勤204, 第2节课, 103
    # 要考勤205(第三个人踢掉队首的代码)

    c = AutoCheckin('w_101')
    c.enter_time = '9:00'
    c.section_id = 1
    c.attach(EndcheckinObserver(c))
    c.attach(TimeWindowObserver(c))
    BaseCheckin.checkin_list.append(c)

    e = AutoCheckin('w_102')
    e.enter_time = '9:05'
    e.section_id = 1
    e.attach(EndcheckinObserver(e))
    e.attach(TimeWindowObserver(e))
    BaseCheckin.checkin_list.append(e)

    d = AutoCheckin('w_103')
    d.attach(EndcheckinObserver(d))
    d.attach(TimeWindowObserver(d))
    d.enter_time = '10:30'
    d.entry_list()
    #
    # 场景5:101
    # 第1节课正在考勤201, 第1节课, 102
    # 正在考勤204, 第2节课, 103
    # 要考勤206(第三个人踢掉中间的代码)

    # c = Autocheckin('w_101')
    # c.enter_time = '8:30'
    # c.section_id = 1
    # checkin.checkin_list.append(c)
    #
    # e = Autocheckin('w_102')
    # e.enter_time = '8:31'
    # e.section_id = 1
    # checkin.checkin_list.append(e)
    #
    # d = Autocheckin('w_103')
    # d.enter_time = '10:40'
    # d.entryList()

    # 场景6:101
    # 第1节课正在考勤201;
    # 102
    # 正在第1节课考勤204;
    # 104
    # 第二节课要考勤(第三个人踢掉前面两个班, 成为队首中间的代码)
    # e = Autocheckin('w_102')
    # e.enter_time = '8:30'
    # e.section_id = 1
    # checkin.checkin_list.append(e)
    #
    # c = Autocheckin('w_101')
    # c.enter_time = '8:31'
    # c.section_id = 1
    # checkin.checkin_list.append(c)
    #
    #
    # print checkin.checkin_list[0].class_list
    # print checkin.checkin_list[1].class_list
    # d = Autocheckin('w_104')
    # d.enter_time = '10:40'
    #
    # print d.class_list
    # d.entryList()













# c = Autocheckin('wonka80')#创建对象,完成考勤对象依赖的初始化
    # 测试多组用户学生在 1全局队列为空 2 时间窗口为5秒 3 在时间窗口之内提交的数据 通过
    # c.startcheckin()
    # c.random_list.append('wfsf_135')
    # c.joincheckin('wfsf_135')
    # c.joincheckin('wfsf_135')
    # c.joincheckin('wfsf_135')
    # c.joincheckin('wfsf_135')
    # c.joincheckin('wfsf_135')
    # c.joincheckin('wfsf_135')
    # c.joincheckin('wfsf_136')
    # c.joincheckin('wfsf_136')
    # c.joincheckin('wfsf_136')
    # c.joincheckin('wfsf_136')
    # c.joincheckin('wfsf_136')
    # c.joincheckin('wfsf_136')
    # c.joincheckin('wfsf_136')
    # c.joincheckin('wfsf_137')
    # c.joincheckin('wfsf_137')
    # c.joincheckin('wfsf_137')
    # c.joincheckin('wfsf_137')
    # c.joincheckin('wfsf_137')
    # c.joincheckin('wfsf_137')
    # c.joincheckin('wfsf_139')
    # c.joincheckin('wfsf_139')
    # c.joincheckin('wfsf_139')
    # c.joincheckin('wfsf_139')
    # c.joincheckin('wfsf_139')
    # c.joincheckin('wfsf_139')
    # c.joincheckin('wfsf_125')
    # c.joincheckin('wfsf_125')
    # c.joincheckin('wfsf_125')
    # c.joincheckin('wfsf_125')
    # c.joincheckin('wfsf_125')
    # c.joincheckin('wfsf_125')
    # c.joincheckin('wfsf_126')
    # c.joincheckin('wfsf_126')
    # c.joincheckin('wfsf_126')
    # c.joincheckin('wfsf_126')
    # c.joincheckin('wfsf_126')
    # c.joincheckin('wfsf_126')
    # c.endcheckin()

    #测试多组用户学生在 1全局队列为空 2 时间窗口为5秒 3 在时间窗口开启之后5秒 再次提交的数据 通过
    # c.startcheckin()
    # c.joincheckin('wfsf_135')
    # c.joincheckin('wfsf_136')
    # c.joincheckin('wfsf_137')
    # c.joincheckin('wfsf_139')
    # time.sleep(6)
    # c.joincheckin('wfsf_125')
    # c.joincheckin('wfsf_126')
    # c.joincheckin('wfsf_128')
    # c.joincheckin('wfsf_127')
    # c.joincheckin('wfsf_129')
    # c.endcheckin()

    # # 测试多组用户学生在 1全局队列不为空 但 节次相同 没有交集 2 时间窗口为5秒 3 在时间窗口开启之后5秒 再次提交的数据 通过
    # c = Autocheckin('wonka80')  # 创建对象,完成考勤对象依赖的初始化
    # # 测试多组用户学生在 1全局队列为空 2 时间窗口为5秒 3 在时间窗口之内提交的数据 通过
    # c.startcheckin()
    # print checkin.checkin_list[0]
    # # 测试多组用户学生在 1全局队列为空 2 时间窗口为5秒 3 在时间窗口之内提交的数据 通过
    # d = Autocheckin('Tp_rt55')
    # d.section_id = 4
    # d.startcheckin()

    # d.crs_id = 11111111
    # self.crs_id = 51610134
    # c.checkin_list.append(d)
    # c.startcheckin()
    # c.joincheckin('wfsf_135')
    # c.joincheckin('wfsf_136')
    # c.joincheckin('wfsf_137')
    # c.joincheckin('wfsf_139')
    # time.sleep(6)
    # c.joincheckin('wfsf_125')
    # c.joincheckin('wfsf_126')
    # c.joincheckin('wfsf_128')
    # c.joincheckin('wfsf_127')
    # c.joincheckin('wfsf_129')
    # c.endcheckin()

    # 测试多组用户学生在 1全局队列为空 2 时间窗口为5秒 3 在时间窗口之内被抽点与抽点的学生依次考勤 通过
    # c.startcheckin()
    # c.startRandomcheckin(15)
    # c.joincheckin('wfsf_119')
    # c.joincheckin('wfsf_118')
    # c.joincheckin('wfsf_117')
    # c.joincheckin('wfsf_116')
    # c.joincheckin('wfsf_115')
    # c.joincheckin('wfsf_129')
    # c.joincheckin('wfsf_128')
    # c.joincheckin('wfsf_127')
    # c.joincheckin('wfsf_126')
    # c.joincheckin('wfsf_125')
    # c.joincheckin('wfsf_139')
    # c.joincheckin('wfsf_138')
    # c.joincheckin('wfsf_137')
    # c.joincheckin('wfsf_136')
    # c.joincheckin('wfsf_135')
    # c.joincheckin('wfsf_109')
    # c.joincheckin('wfsf_108')
    # c.joincheckin('wfsf_107')
    # c.joincheckin('wfsf_106')
    # c.joincheckin('wfsf_105')
    # c.joincheckin('wfsf_99')
    # c.joincheckin('wfsf_98')
    # c.joincheckin('wfsf_97')
    # c.joincheckin('wfsf_96')
    # c.joincheckin('wfsf_95')
    # c.joincheckin('wfsf_89')
    # c.joincheckin('wfsf_88')
    # c.joincheckin('wfsf_87')
    # c.joincheckin('wfsf_86')
    # c.joincheckin('wfsf_85')
    # c.endcheckin()