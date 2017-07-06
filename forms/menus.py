from checkin.forms.main_form import MainForm
from checkin.forms.teacher_form import TeacherForm, UpdateForm, HistoryForm, ProgressForm, StartForm
from checkin.base_checkin import BaseCheckin
from checkin.forms.student_form import StudentForm
from checkin.printinfo import PrtInfo
from checkin.auto_checkin import AutoCheckin
from checkin.man_checkin import ManCheckin
from checkin.internal.base_file.base_file import BaseFile,SumFile,DetailFile


def main_menu():
    while True:
        m = MainForm()
        c = m.init_form()
        if c == 2:
            tea_menu()
        if c == 1:
            join_checkin_menu()
        if c == 3:
            exit(0)


def tea_menu():
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
            break


def start_menu():
    while True:
        m = StartForm()
        c = m.init_form()
        if c == 1:
            start_checkin_menu()
        if c == 2:
            start_manual_checkin()
            pass
        if c == 3:
            break


def update_menu():
    while True:
        m = UpdateForm()
        c = m.init_form()
        if c == 1:
            update_once_checkin()
            pass
        if c == 2:
            break


def progress_menu():
    while True:
        m = ProgressForm()
        c = m.init_form()
        if c == 1:
            attendence()
        if c == 2:
            absence()
        if c == 3:
            detail_now()
            pass
        if c == 4:
            break


def history_menu():
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
            break


def stu_menu():
    while True:
        m = StudentForm()
        c = m.init_form()
        if c == 1:
            join_checkin_menu()
        if c == 2:
            break


def join_checkin_menu():
    while True:
       wechat_id = raw_input(PrtInfo.promptMessage(0))
       t =  BaseCheckin.find_checkin_obj_with_wechat_id(wechat_id)
       if t != None:
           t.join_checkin(wechat_id)
       prompt =  raw_input('maybe try again?(y/n)')
       if prompt == 'n':
            break


def start_checkin_menu():
    while True:
        wechat_id = raw_input(PrtInfo.promptMessage(0))
        obj = AutoCheckin(wechat_id)
        if obj.tea_id == 0:
            print PrtInfo.failedMessage(4)
            prompt = raw_input('maybe try again?(y/n)')
            if prompt == 'n':
                break
        else:
            obj.start_checkin()
            break


def start_manual_checkin():
    while True:
        wechat_id = raw_input(PrtInfo.promptMessage(0))
        obj =ManCheckin(wechat_id)
        if obj.tea_id == 0:
            print PrtInfo.failedMessage(4)
            prompt = raw_input('maybe try again?(y/n)')
            if prompt == 'n':
                break
        else:
            obj.init_detail_records()
            break


def update_once_checkin():
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
            print range(1, obj.init_seq_id(obj.tea_id, obj.crs_id) - 1)
            seq_id = raw_input(PrtInfo.promptMessage(7))
            obj.update_stu_detail_checkin_result(stu_id, seq_id,obj.tea_id,obj.crs_id)
            break


def sum_history():
    while True:
        wechat_id = raw_input(PrtInfo.promptMessage(0))
        obj = ManCheckin(wechat_id)
        if obj.tea_id == 0:
            print PrtInfo.failedMessage(4)
            prompt = raw_input('maybe try again?(y/n)')
            if prompt == 'n':
                break
        else:
            sum_records = SumFile.read_file(BaseCheckin.init_sum_name(obj.tea_id,obj.crs_id))
            print sum_records
            break


def detail_history():
    while True:
        wechat_id = raw_input(PrtInfo.promptMessage(0))
        obj = ManCheckin(wechat_id)
        if obj.tea_id == 0:
            print PrtInfo.failedMessage(4)
            prompt = raw_input('maybe try again?(y/n)')
            if prompt == 'n':
                break
        else:
            print range(1, obj.init_seq_id(obj.tea_id, obj.crs_id) - 1)
            seq_id = raw_input(PrtInfo.promptMessage(7))
            detail_records = DetailFile.read_file(BaseCheckin.init_detail_name(obj.tea_id,obj.crs_id,seq_id))
            print detail_records
            break


def checkin_history():
    while True:
        wechat_id = raw_input(PrtInfo.promptMessage(0))
        obj = ManCheckin(wechat_id)
        if obj.tea_id == 0:
            print PrtInfo.failedMessage(4)
            prompt = raw_input('maybe try again?(y/n)')
            if prompt == 'n':
                break
        else:
            print range(1, obj.init_seq_id(obj.tea_id, obj.crs_id))
            seq_id = raw_input(PrtInfo.promptMessage(7))
            detail_records = DetailFile.read_file(BaseCheckin.init_detail_name(obj.tea_id,obj.crs_id,seq_id))
            print BaseCheckin.filter_invalid_detail_records(detail_records)
            break


def attendence():
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
                for i in detail_records:
                    if i['IsSuc'] == 'True':
                        print i
                break


def absence():
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
                for i in detail_records:
                    if i['IsSuc'] == 'False':
                        print i
                break

def detail_now():
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
                print detail_records
                break


if __name__ == '__main__':
    main_menu()