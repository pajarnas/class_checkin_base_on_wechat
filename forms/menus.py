from checkin.forms.main_form import MainForm
from checkin.forms.base_form import Form
from checkin.forms.teacher_form import TeacherForm, UpdateForm, HistoryForm, ProgressForm, StartForm
from checkin.base_checkin import BaseCheckin
from checkin.forms.student_form import StudentForm
from checkin.printinfo import PrtInfo
from checkin.auto_checkin import AutoCheckin
from checkin.man_checkin import ManCheckin
from checkin.internal.base_file.base_file import BaseFile,SumFile,DetailFile
from checkin.format_print import *
import subprocess


def main_menu():
    subprocess.call("clear")
    while True:
        m = MainForm()
        c = m.init_form()
        if c == 2:
            tea_menu()
        if c == 1:
            stu_menu()
        if c == 3:
            subprocess.call("clear")
            exit(0)


def tea_menu():
    subprocess.call("clear")
    while True:
        m = TeacherForm()
        c = m.init_form()
        if c == 1:
            start_menu()
        if c == 2:
            update_menu()
        if c == 3:
            history_menu()
        if c == 4:
            progress_menu()
        if c == 5:
            subprocess.call("clear")
            break


def start_menu():
    subprocess.call("clear")
    while True:
        m = StartForm()
        c = m.init_form()
        if c == 1:
            start_checkin_menu()
        if c == 2:
            start_manual_menu()
            pass
        if c == 3:
            start_random_menu()
        if c == 4:
            subprocess.call("clear")
            break



def update_menu():
    subprocess.call("clear")
    while True:
        m = UpdateForm()
        c = m.init_form()
        if c == 1:
            update_once_checkin()
            pass
        if c == 2:
            subprocess.call("clear")
            break


def progress_menu():
    subprocess.call("clear")
    while True:
        m = ProgressForm()
        c = m.init_form()
        if c == 1:
            attendence()
        if c == 2:
            absence()
        if c == 3:
            detail_now()
        if c == 4:
            subprocess.call("clear")
            break


def history_menu():
    subprocess.call("clear")
    while True:
        m = HistoryForm()
        c = m.init_form()
        if c == 1:
            sum_history()
        if c == 2:
            detail_history()
        if c == 3:
            checkin_history()
        if c == 4:
            subprocess.call("clear")
            break


def stu_menu():
    subprocess.call("clear")
    while True:
        m = StudentForm()
        c = m.init_form()
        if c == 1:
            join_checkin_menu()
        if c == 2:
            subprocess.call("clear")
            break


def join_checkin_menu():
    subprocess.call("clear")
    while True:
       wechat_id = raw_input(PrtInfo.promptMessage(0))
       t =  BaseCheckin.find_checkin_obj_with_wechat_id(wechat_id)
       if t != None:
           if t.get_random_list() != []:
               print 'Random check in student list :'
               print  t.get_random_list()
           t.join_checkin(wechat_id)
       prompt = raw_input('maybe try again?(y/n)')
       if prompt == 'n':
           subprocess.call("clear")
           break


def start_checkin_menu():
    subprocess.call("clear")
    while True:
        wechat_id = raw_input(PrtInfo.promptMessage(0))
        obj = AutoCheckin(wechat_id)
        if obj == None:
            print PrtInfo.failedMessage(4)
            prompt = raw_input('maybe try again?(y/n)')
            if prompt == 'n':
                break
        else:
            obj.start_checkin()
            break


def start_manual_menu():
    subprocess.call("clear")
    while True:
        wechat_id = raw_input(PrtInfo.promptMessage(0))
        obj = ManCheckin(wechat_id)
        if obj.tea_id == 0:
            print PrtInfo.failedMessage(4)
            prompt = raw_input('maybe try again?(y/n)')
            if prompt == 'n':
                break
        else:
            obj.add_seq_id(obj.seq_id)
            obj.write_detail_file(obj.init_detail_records())
            obj.update_sum_by_certain_seq_id(obj.seq_id)
            break


def start_random_menu():
    subprocess.call("clear")
    while True:
        wechat_id = raw_input(PrtInfo.promptMessage(0))
        obj = BaseCheckin.find_checkin_obj_for_tea(wechat_id)
        if obj == None:
            print PrtInfo.failedMessage(4)
            prompt = raw_input('maybe try again?(y/n)')
            if prompt == 'n':
                subprocess.call("clear")
                break
        else:
            try:
                i = int(raw_input('Please input random number:'))
                obj.start_random_checkin(i)
                break
            except ValueError,e:
                print 'invalid input ,try again'


def update_once_checkin():
    subprocess.call("clear")
    while True:
        wechat_id = raw_input(PrtInfo.promptMessage(0))
        obj =ManCheckin(wechat_id)
        if obj.tea_id == 0:
            print PrtInfo.failedMessage(4)
            prompt = raw_input('maybe try again?(y/n)')
            if prompt == 'n':
                break
        else:
            stu_id = raw_input(PrtInfo.promptMessage(3))
            r = range(1, obj.init_seq_id(obj.tea_id, obj.crs_id))
            r.append('exit')
            c = Form(['seq id'], r)
            seq_id = c.init_form()
            if seq_id == len(r) or seq_id == -1:
                break
            obj.update_stu_detail_checkin_result(stu_id, seq_id,obj.tea_id,obj.crs_id)
            break


def sum_history():
    subprocess.call("clear")
    while True:
        wechat_id = raw_input(PrtInfo.promptMessage(0))
        obj = ManCheckin(wechat_id)
        if obj.tea_id == 0:
            print PrtInfo.failedMessage(4)
            prompt = raw_input('maybe try again?(y/n)')
            if prompt == 'n':
                break
        else:
            BaseCheckin.update_sum(obj)
            sum_records = SumFile.read_file(BaseCheckin.init_sum_name(obj.tea_id,obj.crs_id))
            r = range(1, obj.init_seq_id(obj.tea_id, obj.crs_id))
            r.append('exit')
            q = Form(['seq id'], ['once', 'all', 'back'])
            ch = q.init_form()

            if ch == len(q.items) or ch == -1:
                break
            elif ch == 1:
                c = Form(['seq id'], r)
                seq_id = c.init_form()
                if seq_id == len(r) or seq_id == -1:
                    break
                sum_format(sum_records, seq_id=seq_id)
                break
            sum_format(sum_records)
            break


def detail_history():
    subprocess.call("clear")
    while True:
        wechat_id = raw_input(PrtInfo.promptMessage(0))
        obj = ManCheckin(wechat_id)
        if obj.tea_id == 0:
            print PrtInfo.failedMessage(4)
            prompt = raw_input('maybe try again?(y/n)')
            if prompt == 'n':
                break
        else:
            r = range(1, obj.init_seq_id(obj.tea_id, obj.crs_id))
            r.append('exit')
            c = Form(['seq id'], r)
            seq_id = c.init_form()
            if seq_id == len(r) or seq_id == -1:
                break
            detail_records = DetailFile.read_file(BaseCheckin.init_detail_name(obj.tea_id,obj.crs_id,seq_id))
            detail_format(detail_records)
            break


def checkin_history():
    subprocess.call("clear")
    while True:
        wechat_id = raw_input(PrtInfo.promptMessage(0))
        obj = ManCheckin(wechat_id)
        if obj.tea_id == 0:
            print PrtInfo.failedMessage(4)
            prompt = raw_input('maybe try again?(y/n)')
            if prompt == 'n':
                break
        else:
            r = range(1,obj.init_seq_id(obj.tea_id, obj.crs_id) )
            r.append('exit')
            print len(r)
            c = Form(['seq id'],r)
            seq_id = c.init_form()
            if seq_id == len(r) or seq_id == -1:
                break
            detail_records = DetailFile.read_file(BaseCheckin.init_detail_name(obj.tea_id,obj.crs_id,seq_id))
            detail_format(BaseCheckin.filter_invalid_detail_records(detail_records))
            break


def attendence():
    subprocess.call("clear")
    while True:
        wechat_id = raw_input(PrtInfo.promptMessage(0))
        obj = ManCheckin(wechat_id)
        if obj.tea_id == 0:
            print PrtInfo.failedMessage(4)
            prompt = raw_input('maybe try again?(y/n)')
            if prompt == 'n':
                break
        else:
            c = BaseCheckin.find_checkin_obj_for_tea(wechat_id)
            if c != None:
                detail_records = BaseFile.read_file(c.init_detail_name(str(c.tea_id),str(c.crs_id),str(c.seq_id)))
                detail_records = BaseCheckin.filter_invalid_detail_records(detail_records)
                temp = []
                for i in detail_records:
                    if i['IsSuc'] == 'True':
                        temp.append(i)
                print detail_format(temp)
                break
            else:
                break


def absence():
    subprocess.call("clear")
    while True:
        wechat_id = raw_input(PrtInfo.promptMessage(0))
        obj = ManCheckin(wechat_id)
        if obj.tea_id == 0:
            print PrtInfo.failedMessage(4)
            prompt = raw_input('maybe try again?(y/n)')
            if prompt == 'n':
                break
        else:
            c = BaseCheckin.find_checkin_obj_for_tea(wechat_id)
            if c != None:
                detail_records = BaseFile.read_file(c.init_detail_name(str(c.tea_id),str(c.crs_id),str(c.seq_id)))
                detail_records = BaseCheckin.filter_invalid_detail_records(detail_records)
                temp = []
                for i in detail_records:
                    if i['IsSuc'] == 'False':
                        temp.append(i)
                print detail_format(temp)
                break
            else:
                break


def detail_now():
    subprocess.call("clear")
    while True:
        wechat_id = raw_input(PrtInfo.promptMessage(0))
        obj = ManCheckin(wechat_id)
        if obj.tea_id == 0:
            print PrtInfo.failedMessage(4)
            prompt = raw_input('maybe try again?(y/n)')
            if prompt == 'n':
                break
        else:
            c = BaseCheckin.find_checkin_obj_for_tea(wechat_id)
            if c != None:
                detail_records = BaseFile.read_file(c.init_detail_name(str(c.tea_id),str(c.crs_id),str(c.seq_id)))
                detail_format(detail_records)
                break
            else:
                break


if __name__ == '__main__':
    main_menu()