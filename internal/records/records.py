class Records():
    def __init__(self):
        pass

class SumRecord(Records):
    def __init__(self,stu_id,seq_list):
        Records.__init__()
        self.stu_id = stu_id
        self.seq_list = seq_list

class DetailRecord(Records):
    def __init__(self,stu_id,path,checkin_type,is_suc,checkin_result):
        Records.__init__()
        self.stu_id = stu_id
        self.path = path
        self.checkin_type = checkin_type
        self.checkin_result = checkin_result
        self.is_suc = is_suc

class SqeRecord(Records):
    def __init__(self,tea_id,crs_id,seq_id,date_time):
        Records.__init__()
        self.tea_id = tea_id
        self.crs_id = crs_id
        self.seq_id = seq_id
        self.date_time = date_time

class StudentRecord(Records):
    def __init__(self,class_name,wechat_id,path,id,name):
        Records.__init__()
        self.class_name = class_name
        self.wechat_id = wechat_id
        self.path = path
        self.name = name
        self.id = id
class TeacherRecord(Records):
    def __init__(self,wechat_id,id):
        Records.__init__()
        self.wechat_id = wechat_id
        self.id = id

class CourseRecord(Records):
    def __init__(self,id,tea_id,class_name,name):
        Records.__init__()
        self.id = id
        self.name = name
        self.class_name =class_name
        self.tea_id = tea_id

