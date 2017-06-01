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
        self.detail_records = self.initDetailRecords()
        self.class_list = self.initClassList()
        self.random_list = []
        self.section_id = self.initSectionId(time.strftime('%H%M'))


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
        nowtime = int(nowtime)
        for i in range(0, 5, 1):
            e = int(t.class_time_list[i]['EndTime'])
            s = int(t.class_time_list[i]['StartTime'])
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
        self.section_id = self.initSectionId(time.strftime('%H%M'))
        # 否:直接提示现在无法考勤
        if self.section_id == 0:
            raise NouFoundException, PrtInfo.failedMessage(3)

        # 建立一个Timer计时器的实例
        ti = Timer()
        # 空还是非空?:

        #非空:
        if Checkin.checkin_list != []:
            # 当前节次是否与队首的相同?

            # 相同
            if self.section_id == Checkin.checkin_list[0].section_id:
                #有交集:无法进入
                for checkin_obj in Checkin.checkin_list:
                    if (set(self.class_list) & set(checkin_obj.class_list)):
                        raise WrongException,PrtInfo.failedMessage(2)

                # 无交集:进入队列, 与之前进入的一同退出
                Checkin.checkin_list.append(self)
                print PrtInfo.successMessage(7)
                return True

            # 不相同
            else:
                # 清空队列, 销毁计时器, 重新开始打开计时器
                print PrtInfo.successMessage(6)
                ti.clearList()
                Checkin.checkin_list.append(self)
                ti.startTimerThreading(5)
                return True

        # 空 :
        else:
            print PrtInfo.successMessage(7)
            Checkin.checkin_list.append(self)
            ti.startTimerThreading(5)
            return True


    def getStuIdInClassList(self,wechat_id):
        for stu_rec in self.student_records:
            if stu_rec['WeChatID'] == wechat_id:
                return stu_rec['StuID']
        else:
            raise NouFoundException,PrtInfo.notFoundMessage(3)


    def uploadPath(self):
        return raw_input(PrtInfo.promptMessage(5))

    def judgeResult(self):
        # isLate(time)
        # isHere(path)
        # isYourself(path)
        i = random.randrange(0, 3)
        if i == 0 :
            return 'Abnormal'
        if i == 1 :
            return 'Normal'
        if i == 2 :
            return 'Late'

    def getCheckinResult(self,checkin_type,judge_result,ori_result):
        if (ori_result == '缺勤') & (checkin_type == 'Auto' )& (judge_result == 'Normal'):
            return {'checkinResult':'出勤'}
        if (ori_result == '出勤') & (checkin_type == 'Auto') :
            return {'checkinResult':'出勤'}
        if (ori_result == '缺勤') & (checkin_type == 'Auto' )& (judge_result == 'Abnormal'):
            return {'checkinResult':'缺勤'}
        if (ori_result == '缺勤') & (checkin_type == 'Auto') & (judge_result == 'Late'):
            return '迟到'
        if (ori_result == '假条提交') :
            return '假条提交'
        if (ori_result == '早退') & (checkin_type == 'Random') &( (judge_result == 'Abnormal')|(judge_result == 'Late') ):
            return '早退'
        if (ori_result == '早退') & (checkin_type == 'Random') & (judge_result == 'Normal'):
            return '出勤'
        return '异常'


    def getDetailRecord(self,checkin_type,ori_result):
        judge_result = self.judgeResult()
        if judge_result == 'Normal' :
            is_suc = 'True'
        else :
            is_suc = 'False'
        return { 'checkinTime': time.strftime('%Y-%m-%d %H:%M:%S'),
                                'ProofPath': 'self.uploadPath()',
                                'checkinType': checkin_type,
                                'IsSuc':is_suc,
                                'checkinResult': self.getCheckinResult(checkin_type,judge_result,ori_result) }

    def initNewDetailRecord(self,wechat_id):
        # checkin_type = raw_input(PrtInfo.promptMessage(6))
        checkin_type = 'Auto'
        #######for test
        if wechat_id  in self.random_list:
            checkin_type = 'Random'
        ######## for test
        if checkin_type == 'Random':
            if wechat_id not in self.random_list:
                print PrtInfo.notFoundMessage(4)
        stu_id = self.getStuIdInClassList(wechat_id)
        PrtInfo.tipsMessage(1)
        for detail_rec in self.detail_records:
            if detail_rec['StuID'] == stu_id :
                temp_dict = self.getDetailRecord(checkin_type,detail_rec['checkinResult'])
                detail_rec.update(temp_dict)
                return True
        else:
            print PrtInfo.failedMessage(1)


    def startCheckin(self):
        if (self.entryList() != False):
            # 将初始化的sum_records和detail_records 写入两个文件
            self.createDetailFiles()
            self.createSumFiles()
            self.insertNewSeqRecord()


    def joinCheckin(self,wechat_id):
        if self in Checkin.checkin_list:
            self.initNewDetailRecord(wechat_id)
            PrtInfo.successMessage(8)
        else:
            print PrtInfo.failedMessage(0)

    def randomCheckin(self,num):
        temp_list = random.sample(self.student_records, num)
        for line in temp_list:
            self.random_list.append(line['WeChatID'])
        for line in self.student_records:
            if line['WeChatID'] in self.random_list:
                for detail_rec in self.detail_records:
                    if line['StuID'] == detail_rec['StuID']:
                        detail_rec['checkinResult'] = '早退'


    def endCheckin(self):
        self.createDetailFiles()
        self.createSumFiles()

    def exitCheckin(self):
        pass








if __name__ == '__main__':
    c = AutoCheckin('wonka80')#创建对象,完成考勤对象依赖的初始化
    # 测试多组用户学生在 1全局队列为空 2 时间窗口为5秒 3 在时间窗口之内提交的数据 通过
    # c.startCheckin()
    # c.joinCheckin('wfsf_135')
    # c.joinCheckin('wfsf_136')
    # c.joinCheckin('wfsf_137')
    # c.joinCheckin('wfsf_139')
    # c.joinCheckin('wfsf_125')
    # c.joinCheckin('wfsf_126')
    # c.joinCheckin('wfsf_128')
    # c.joinCheckin('wfsf_127')
    # c.joinCheckin('wfsf_129')
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
    # d = AutoCheckin('Tp_rt55')
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
    c.startCheckin()
    c.randomCheckin(15)
    c.joinCheckin('wfsf_119')
    c.joinCheckin('wfsf_118')
    c.joinCheckin('wfsf_117')
    c.joinCheckin('wfsf_116')
    c.joinCheckin('wfsf_115')
    c.joinCheckin('wfsf_129')
    c.joinCheckin('wfsf_128')
    c.joinCheckin('wfsf_127')
    c.joinCheckin('wfsf_126')
    c.joinCheckin('wfsf_125')
    c.joinCheckin('wfsf_139')
    c.joinCheckin('wfsf_138')
    c.joinCheckin('wfsf_137')
    c.joinCheckin('wfsf_136')
    c.joinCheckin('wfsf_135')
    c.joinCheckin('wfsf_109')
    c.joinCheckin('wfsf_108')
    c.joinCheckin('wfsf_107')
    c.joinCheckin('wfsf_106')
    c.joinCheckin('wfsf_105')
    c.joinCheckin('wfsf_99')
    c.joinCheckin('wfsf_98')
    c.joinCheckin('wfsf_97')
    c.joinCheckin('wfsf_96')
    c.joinCheckin('wfsf_95')
    c.joinCheckin('wfsf_89')
    c.joinCheckin('wfsf_88')
    c.joinCheckin('wfsf_87')
    c.joinCheckin('wfsf_86')
    c.joinCheckin('wfsf_85')
    c.endCheckin()