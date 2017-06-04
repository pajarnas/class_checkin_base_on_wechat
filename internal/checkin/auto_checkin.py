#encoding=utf-8
from internal.base_file.base_file import BaseFile,DetailFile,SumFile,CourseFile
from checkin import Checkin
from printinfo import PrtInfo
from my_exceptions import NouFoundException,WrongException
from __init__ import ReadIni
from timewindow import Timer
import time,random,threading
class AutoCheckin (Checkin):

    def __init__(self,wechat_id):
        Checkin.__init__(self,wechat_id)
        self.class_list = self.initClassList()
        self.random_list = []
        self.enter_time = time.strftime('%H:%M')
        self.section_id = self.initSectionId(time.strftime('%H:%M'))


    def initClassList(self):
            crs_list = CourseFile.read_file(Checkin.coures_file.name)
            class_list = []
            for crs_rec in  crs_list:
                if (crs_rec['TeacherID'] == str(self.tea_id)) & (crs_rec['CourseID'] == str(self.crs_id)):
                    class_list.append(crs_rec['ClassNums'])
            if class_list == []:
                raise NouFoundException,PrtInfo.notFoundMessage(5)
            return class_list

    def initSectionId(self,nowtime):
        t = ReadIni()
        nowtime = int(''.join(nowtime.split(':')))
        for i in range(0, 5, 1):
            e = int(''.join(t.class_time_list[i]['EndTime'].split(':')))
            s = int(''.join(t.class_time_list[i]['StartTime'].split(':')))
            if (nowtime >= s) & (nowtime <= e):
                return i + 1
        else:
            return 0

    def initDetailRecords(self):
        stu_records = BaseFile.read_file(Checkin.student_file.name)
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

    def entryList(self):
        # 系统时间是否在节次区间
        self.enter_time = time.strftime('%H:%M')
        # self.section_id = self.initSectionId(time.strftime('%H:%M'))
        class_list = self.initClassList()
        intersection_flag = False
        # 建立一个Timer计时器的实例
        ti = Timer()
        # 全局队列为空:
        if Checkin.checkin_list == []:
            print PrtInfo.successMessage(7)
            Checkin.checkin_list.append(self)
            ti.startTiming()
            return True
        # 非空
        kick_head = False
        for checkin_obj in Checkin.checkin_list:
            if (set(class_list) & set(checkin_obj.class_list)):
            # 存在交集
                # 节次不一样 踢掉
                if self.section_id != checkin_obj.section_id:

                    intersection_flag = True
                    if Checkin.checkin_list.index(checkin_obj) == 0:
                        # 踢掉的是队首
                        kick_head = True
                    print PrtInfo.successMessage(6)
                    Checkin.checkin_list.remove(checkin_obj)
                # 节次一样,无法进入,退出函数
                else:
                    return False
                    #raise WrongException, PrtInfo.failedMessage(2)
        # 队列中的所有班都与来者没有交集,或者有交集被踢出去
        if (intersection_flag == False) | (kick_head == False):
            # 没有交集 或者 踢掉的不是队首
             print PrtInfo.successMessage(7)
             Checkin.checkin_list.append(self)
             ti.justWaiting()
        elif (intersection_flag == True) & (kick_head == True) & \
                (Checkin.checkin_list.__len__() != 0):
            # 有交集 且 踢掉的是队首 且 当前者不是队首
            print PrtInfo.successMessage(7)
            Checkin.checkin_list.append(self)
            t2 = Checkin.checkin_list[0].enter_time
            t3 = Checkin.checkin_list[1].enter_time
            ti.timeSecond(t2,t3)
        else:
            # 有交集 且 踢掉队首 且 自己是队首
            print PrtInfo.successMessage(7)
            Checkin.checkin_list.append(self)
            ti.startTiming()

    def getStuIdInClassList(self,wechat_id):
        student_records = self.initStudentRecords()
        for stu_rec in student_records:
            if stu_rec['WeChatID'] == wechat_id:
                return stu_rec['StuID']
        else:
            raise NouFoundException,PrtInfo.notFoundMessage(3)


    def uploadPath(self):
        return raw_input(PrtInfo.promptMessage(5))

    def judgeResult(self,proof_path):
        # isLate(time)
        # isHere(path)
        # isYourself(path)
        i = random.randrange(0, 2)
        if i == 0 :
            return 'True'
        if i == 1 :
            return 'False'


    def getDetailRecord(self,checkin_type,stu_id):
        judge_result = self.judgeResult('self.uploadPath()')
        return { 'StuID': stu_id,
                 'checkinTime': time.strftime('%Y-%m-%d %H:%M:%S'),
                                'ProofPath': self.uploadPath(),
                                'checkinType': checkin_type,
                                'IsSuc':judge_result,
                                'checkinResult': 'none' }

    def getLatestRecord(self,stu_id):
        detail_rec = {}
        detail_records = BaseFile.read_file(self.initDetailName(self.tea_id,self.crs_id,self.seq_id))
        for rec in detail_records:
            if rec['StuID'] == str(stu_id):
                detail_rec = rec
        return detail_rec

    def initNewDetailRecord(self,wechat_id,checkin_type):
        # 先判断最新记录是否是True
        stu_id = self.getStuIdInClassList(wechat_id)
        rec = self.getLatestRecord(stu_id)
        if rec == {}:
            DetailFile(self.initDetailName(self.tea_id, self.crs_id, self.seq_id)). \
                write_file([self.getDetailRecord(checkin_type, stu_id)], 'ab')
            return
        elif (rec['IsSuc'] != 'True'):
            DetailFile(self.initDetailName(self.tea_id, self.crs_id, self.seq_id)). \
                write_file([self.getDetailRecord(checkin_type, stu_id)], 'ab')
            return
        else:
            return

    def startCheckin(self):
        if (self.entryList() != False):
            self.createDetailFile([])
            self.updateSumByCertaiSeqId(self.seq_id)
            self.addSeqId(self.seq_id)  # 在seq文件中保存此次seq id 记录

    def joinCheckin(self,wechat_id):
        if self in Checkin.checkin_list:
            checkin_type = 'Auto'
            # checkin_type = raw_input(PrtInfo.promptMessage(6))
            if checkin_type == 'Auto':
                self.initNewDetailRecord(wechat_id,'Auto')
                PrtInfo.successMessage(8)
                return True
            elif checkin_type == 'Random':
                if wechat_id not in self.random_list:
                    print PrtInfo.notFoundMessage(4)
                    return False
                else:
                    self.initNewDetailRecord(wechat_id,'Random')
                    PrtInfo.successMessage(8)
            else:
                print PrtInfo.failedMessage(1)
        else:
            print PrtInfo.failedMessage(0)
            return False

    def startRandomCheckin(self,num):
        student_records =self.initStudentRecords()
        temp_list = random.sample(student_records, num)
        for line in temp_list:
            self.random_list.append(line['WeChatID'])
        for line in student_records:
            if line['WeChatID'] in self.random_list:
                temp_dict = {'StuID': line['StuID'],
                             'checkinTime': time.strftime('%Y-%m-%d %H:%M:%S'),
                             'ProofPath': 'none',
                             'checkinType': 'Random',
                             'IsSuc':'none' ,
                             'checkinResult': '缺勤'
                             }
                DetailFile(self.initDetailName(self.tea_id,self.crs_id,self.seq_id)).write_file([temp_dict],'ab')

    def isLate(self,rec):
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


    def endCheckin(self):
        detail_file = DetailFile(self.initDetailName(self.tea_id,self.crs_id,self.seq_id))
        leave_list =[]
        for stu in self.initStudentRecords():
            rec = self.getLatestRecord(stu['StuID'])
            # 没有签到的学生 缺勤 追加到文件中
            if rec == {}:
                rec = {'StuID': stu['StuID'],
                        'checkinTime': time.strftime('%Y-%m-%d %H:%M:%S'),
                        'ProofPath': 'none',
                        'checkinType': 'Auto',
                        'IsSuc': 'none',
                        'checkinResult': '缺勤'}
            # 签到 并且来的学生 检查是否 迟到
            if rec['ProofPath'] == '假条提交':
                rec.update({'checkinResult': '假条提交'})
                leave_list.append(rec)
            # 签到 并且来的学生 检查是否 迟到
            if rec['IsSuc'] == 'True':
                rec.update({'checkinResult': self.isLate(rec)})

            # 签到失败 没来的学生 记录为缺勤或者早退
            if rec['IsSuc'] == 'False':
                if rec['checkinType'] == 'Random':
                    rec.update({'checkinResult': '早退'})
                else:
                    rec.update({'checkinResult': '缺勤'})
            detail_file.write_file([rec],'ab')
        if leave_list != []:
            print 'You have '+str(leave_list.__len__())+' leave events to handle!'
            for line in leave_list:
                if raw_input(PrtInfo.promptMessage(8)) == 'y':
                    line['checkinResult'] = '请假'
                else:
                    line['checkinResult'] = '缺勤'
                detail_file.write_file([line], 'ab')
        self.updateSum()


    def exitCheckin(self):
        pass

if __name__ == '__main__':
    # c = AutoCheckin('wonka80')#创建对象,完成考勤对象依赖的初始化
    # 测试多组用户学生在 1全局队列为空 2 时间窗口为5秒 3 在时间窗口之内提交的数据 通过
    # c.startCheckin()
    # c.random_list.append('wfsf_135')
    # c.joinCheckin('wfsf_135')
    # c.joinCheckin('wfsf_135')
    # c.joinCheckin('wfsf_135')
    # c.joinCheckin('wfsf_135')
    # c.joinCheckin('wfsf_135')
    # c.joinCheckin('wfsf_135')
    # c.joinCheckin('wfsf_136')
    # c.joinCheckin('wfsf_136')
    # c.joinCheckin('wfsf_136')
    # c.joinCheckin('wfsf_136')
    # c.joinCheckin('wfsf_136')
    # c.joinCheckin('wfsf_136')
    # c.joinCheckin('wfsf_136')
    # c.joinCheckin('wfsf_137')
    # c.joinCheckin('wfsf_137')
    # c.joinCheckin('wfsf_137')
    # c.joinCheckin('wfsf_137')
    # c.joinCheckin('wfsf_137')
    # c.joinCheckin('wfsf_137')
    # c.joinCheckin('wfsf_139')
    # c.joinCheckin('wfsf_139')
    # c.joinCheckin('wfsf_139')
    # c.joinCheckin('wfsf_139')
    # c.joinCheckin('wfsf_139')
    # c.joinCheckin('wfsf_139')
    # c.joinCheckin('wfsf_125')
    # c.joinCheckin('wfsf_125')
    # c.joinCheckin('wfsf_125')
    # c.joinCheckin('wfsf_125')
    # c.joinCheckin('wfsf_125')
    # c.joinCheckin('wfsf_125')
    # c.joinCheckin('wfsf_126')
    # c.joinCheckin('wfsf_126')
    # c.joinCheckin('wfsf_126')
    # c.joinCheckin('wfsf_126')
    # c.joinCheckin('wfsf_126')
    # c.joinCheckin('wfsf_126')
    # c.endCheckin()

    #测试多组用户学生在 1全局队列为空 2 时间窗口为5秒 3 在时间窗口开启之后5秒 再次提交的数据 通过
    # c.startCheckin()
    # c.joinCheckin('wfsf_135')
    # c.joinCheckin('wfsf_136')
    # c.joinCheckin('wfsf_137')
    # c.joinCheckin('wfsf_139')
    # time.sleep(6)
    # c.joinCheckin('wfsf_125')
    # c.joinCheckin('wfsf_126')
    # c.joinCheckin('wfsf_128')
    # c.joinCheckin('wfsf_127')
    # c.joinCheckin('wfsf_129')
    # c.endCheckin()

    # 测试多组用户学生在 1全局队列不为空 但 节次相同 没有交集 2 时间窗口为5秒 3 在时间窗口开启之后5秒 再次提交的数据 通过
    c = AutoCheckin('wonka80')  # 创建对象,完成考勤对象依赖的初始化
    # 测试多组用户学生在 1全局队列为空 2 时间窗口为5秒 3 在时间窗口之内提交的数据 通过
    c.startCheckin()
    print Checkin.checkin_list[0]
    # 测试多组用户学生在 1全局队列为空 2 时间窗口为5秒 3 在时间窗口之内提交的数据 通过
    d = AutoCheckin('Tp_rt55')
    d.section_id = 4
    d.startCheckin()

    # d.crs_id = 11111111
    # self.crs_id = 51610134
    # c.checkin_list.append(d)
    # c.startCheckin()
    # c.joinCheckin('wfsf_135')
    # c.joinCheckin('wfsf_136')
    # c.joinCheckin('wfsf_137')
    # c.joinCheckin('wfsf_139')
    # time.sleep(6)
    # c.joinCheckin('wfsf_125')
    # c.joinCheckin('wfsf_126')
    # c.joinCheckin('wfsf_128')
    # c.joinCheckin('wfsf_127')
    # c.joinCheckin('wfsf_129')
    # c.endCheckin()

    # 测试多组用户学生在 1全局队列为空 2 时间窗口为5秒 3 在时间窗口之内被抽点与抽点的学生依次考勤 通过
    # c.startCheckin()
    # c.startRandomCheckin(15)
    # c.joinCheckin('wfsf_119')
    # c.joinCheckin('wfsf_118')
    # c.joinCheckin('wfsf_117')
    # c.joinCheckin('wfsf_116')
    # c.joinCheckin('wfsf_115')
    # c.joinCheckin('wfsf_129')
    # c.joinCheckin('wfsf_128')
    # c.joinCheckin('wfsf_127')
    # c.joinCheckin('wfsf_126')
    # c.joinCheckin('wfsf_125')
    # c.joinCheckin('wfsf_139')
    # c.joinCheckin('wfsf_138')
    # c.joinCheckin('wfsf_137')
    # c.joinCheckin('wfsf_136')
    # c.joinCheckin('wfsf_135')
    # c.joinCheckin('wfsf_109')
    # c.joinCheckin('wfsf_108')
    # c.joinCheckin('wfsf_107')
    # c.joinCheckin('wfsf_106')
    # c.joinCheckin('wfsf_105')
    # c.joinCheckin('wfsf_99')
    # c.joinCheckin('wfsf_98')
    # c.joinCheckin('wfsf_97')
    # c.joinCheckin('wfsf_96')
    # c.joinCheckin('wfsf_95')
    # c.joinCheckin('wfsf_89')
    # c.joinCheckin('wfsf_88')
    # c.joinCheckin('wfsf_87')
    # c.joinCheckin('wfsf_86')
    # c.joinCheckin('wfsf_85')
    # c.endCheckin()