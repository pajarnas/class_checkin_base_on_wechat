#encoding=utf-8
from checkin.internal.base_file.base_file import BaseFile,DetailFile
from base_checkin import BaseCheckin
from man_checkin import ManCheckin
from subject_observer import EndcheckinObserver,TimeWindowObserver
from checkin.printinfo import PrtInfo
from checkin.internal.checkin_files import ReadIni
from time_window import TimeWindow
import random, time


class AutoCheckin(BaseCheckin):

    def __init__(self, wechat_id):
        BaseCheckin.__init__(self, wechat_id)
        self.class_list = self.init_class_records()
        self.enter_time = time.strftime('%H:%M')
        self.section_id = self.init_section_id(time.strftime('%H:%M'))
        self.time_window = TimeWindow()

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
                             'ProofPath':'Auto',
                             'checkinType':'Auto',
                             'IsSuc':'False',
                             'checkinResult':'缺勤'
                             }
                temp_list.append(temp_dict)
        print PrtInfo.successMessage(3)
        return temp_list

    def entry_list(self):
        # self.enter_time = '8:30'
        self.section_id = self.init_section_id(self.enter_time)
        class_list = self.init_class_records()
        intersection_flag = False

        # 全局队列为空:
        if BaseCheckin.checkin_list == []:
            # print PrtInfo.successMessage(7)
            BaseCheckin.checkin_list.append(self)
            self.time_window.start_timing(300)
            return True
        # 非空
        kick_head = False
        for checkin_obj in BaseCheckin.checkin_list[:]:
            try:
                if set(class_list) & set(checkin_obj.class_list):
                    # 存在交集
                    # 节次不一样 踢掉
                    if self.section_id != checkin_obj.section_id:
                        intersection_flag = True
                        if BaseCheckin.checkin_list.index(checkin_obj) == 0:
                            # 踢掉的是队首
                            kick_head = True
                        checkin_obj.notify()
                        BaseCheckin.checkin_list.remove(checkin_obj)
                    # 节次一样,无法进入,退出函数
                    else:
                        return False
            except TypeError:
                print 'invalid operation'
                return False
        # 队列中的所有班都与来者没有交集,或者有交集被踢出去
        if (intersection_flag is False) | (kick_head is False):
            # 没有交集 或者 踢掉的不是队首
            self.time_window.just_waiting()
            BaseCheckin.checkin_list.append(self)
        elif (intersection_flag is True) & (kick_head is True) & \
                (BaseCheckin.checkin_list.__len__() is not 0):
            # 有交集 且 踢掉的是队首 且 当前者不是队首
            print PrtInfo.successMessage(7)
            BaseCheckin.checkin_list.append(self)
            t2 = BaseCheckin.checkin_list[0].enter_time
            t3 = BaseCheckin.checkin_list[1].enter_time
            self.time_window.time_second(t2, t3)
        else:
            # 有交集 且 踢掉队首 且 自己是队首
            print PrtInfo.successMessage(7)
            BaseCheckin.checkin_list.append(self)
            self.time_window.start_timing()

    def get_stu_id_in_class_list(self, wechat_id):
        student_records = self.init_student_records()
        for stu_rec in student_records:
            if stu_rec['WeChatID'] == wechat_id:
                return stu_rec['StuID']
        else:
            print PrtInfo.notFoundMessage(3)
            return None

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

    def cancel_leave(self, stu_id):
        dict = {'StuID': stu_id,
         'checkinTime': time.strftime('%Y-%m-%d %H:%M:%S'),
         'ProofPath': '',
         'checkinType': 'Auto',
         'IsSuc': 'False',
         'checkinResult': ''}
        DetailFile(self.init_detail_name(self.tea_id, self.crs_id, self.seq_id)). \
            write_file([dict], 'ab')
        print 'please finish your check in'

    def get_detail_record(self, checkin_type, stu_id):
        checkin_result = None
        if raw_input("enter 'y' to ask for leave") == 'y':
            checkin_result = '假条提交'
            print 'the leave permission uploaded'
            proof = self.upload_path()
            judge_result = 'True'
        else:
            proof = self.upload_path()
            judge_result = self.judge_result(proof)
            if judge_result != 'True':
                 print "you are not 'here' or you are not 'you'"
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
            if (rec['StuID'] == str(stu_id)) & (rec['checkinType'] == str(checkin_type)):
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
        elif rec['IsSuc'] != 'True':
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
            checkin_type = raw_input(PrtInfo.promptMessage(6))
            if checkin_type == 'Auto':
                self.init_new_detail_record(wechat_id,'Auto')
                PrtInfo.successMessage(8)
                return True
            elif checkin_type == 'Random':
                random_list = self.get_random_list()
                if random_list == []:
                    print 'No random check in now'
                    return False
                if self.get_stu_id_in_class_list(wechat_id) not in random_list:
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
            if rec['checkinType'] == 'Random' and rec['checkinResult'] == 'init':
                random_list.append(rec['StuID'])
        return random_list

    def start_random_checkin(self,num):
        student_records = self.init_student_records()
        temp_list = random.sample(student_records, num)
        for line in student_records:
            if line in temp_list:
                temp_dict = {'StuID': line['StuID'],
                             'checkinTime': time.strftime('%Y-%m-%d %H:%M:%S'),
                             'ProofPath': 'Auto',
                             'checkinType': 'Random',
                             'IsSuc':'none' ,
                             'checkinResult': 'init'
                             }
                DetailFile(self.init_detail_name(self.tea_id,self.crs_id,self.seq_id)).write_file([temp_dict],'ab')

    def is_late(self, rec):
        checkin_time = ((rec['checkinTime'].split(' '))[1])[0:5]
        dev = int(self.time_window.dev(self.enter_time, checkin_time))
        t = ReadIni()
        if dev < t.read_late_dev():
           return '出勤'
        else:
           return '迟到'

    def get_compared_record(self, auto_rec, ran_rec, is_late):
        if auto_rec['IsSuc'] == ran_rec['IsSuc']:
            checkin_result = '出勤' if auto_rec['IsSuc'] == 'True' else '缺勤'
            auto_rec.update({'checkinResult': checkin_result})
        else:
            t1 = ((auto_rec['checkinTime'].split(' '))[1])[0:5]
            t2 = ((ran_rec['checkinTime'].split(' '))[1])[0:5]
            dev_time = int(self.time_window.dev(t1, t2))
            if is_late:
                if auto_rec['IsSuc'] == 'False' and dev_time > 0:
                    auto_rec.update({'checkinResult':'早退'})
                else:
                    auto_rec.update({'checkinResult':'迟到'})
            else:
                if auto_rec['IsSuc'] == 'True' and dev_time < 0:
                    auto_rec.update({'checkinResult':'早退'})
                else:
                    auto_rec.update({'checkinResult':'出勤'})
        return auto_rec

    def exit_checkin(self):
        pass

    def end_checkin(self):
        detail_file = DetailFile(self.init_detail_name(self.tea_id, self.crs_id, self.seq_id))
        for stu in self.init_student_records():
            auto_rec = self.get_latest_record(stu['StuID'],'Auto')
            ran_rec = self.get_latest_record(stu['StuID'],'Random')
            # 没有签到的学生 缺勤 追加到文件中
            if auto_rec == {}:
                if ran_rec == {}:
                    auto_rec = {'StuID': stu['StuID'],
                           'checkinTime': time.strftime('%Y-%m-%d %H:%M:%S'),
                           'ProofPath': 'none',
                           'checkinType': 'Auto',
                           'IsSuc': 'False',
                           'checkinResult': '缺勤'}
                    detail_file.write_file([auto_rec], 'ab')
                    continue
                else:
                    auto_rec = ran_rec

            # 签到 并且来的学生 检查是否请假
            if auto_rec != {} and auto_rec['checkinResult'] == '假条提交' :
                continue
            # 得到迟到标记,自助考勤最新记录,抽点考勤最新记录
            if ran_rec == {}:
                if auto_rec['IsSuc'] == 'True':
                    auto_rec.update({'checkinResult':self.is_late(auto_rec)})
                else:
                    auto_rec.update({'checkinResult': '缺勤'})
                detail_file.write_file([auto_rec], 'ab')
                continue
            else:
                is_late = True if self.is_late(auto_rec) == '迟到' else False
                auto_rec = self.get_compared_record(auto_rec, ran_rec, is_late)
                detail_file.write_file([auto_rec], 'ab')
        ManCheckin.confirm_leave(self, detail_file)
        self.update_sum()


if __name__ == '__main__':
    c = AutoCheckin('w_101')
    c.seq_id = 14
    c.end_checkin()
