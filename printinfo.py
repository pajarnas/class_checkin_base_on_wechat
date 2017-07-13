class PrtInfo():
    def __init__(self):
        pass

    @staticmethod
    def notFoundMessage(id):
        if id == 1:
            return 'sorry,the teacher has no such course id'
        if id == 2:
            return 'sorry,the course id not in the list'
        if id == 3:
            return 'sorry,the student id not exist'
        if id == 4:
            return 'sorry,you are not in random checkin_files in list'
        if id == 5:
            return 'Not Found (5):'+'no class on lesson'



    @staticmethod
    def promptMessage(id):
        if id == 1:
            return 'please input the course id'
        if id == 2:
            return 'the total course list:'
        if id == 3:
            return 'please input the student id'
        if id == 4:
            return 'please input the check in result of student '
        if id == 5:
            return 'please upload your proof'
        if id == 6:
            return 'please input your check in type (Auto/Random)'
        if id == 7:
            return 'please enter the seq id of check in detail file'
        if id == 8:
            return 'please confirm the leave result (y/n)'
        if id == 0:
            return 'please input your wechat id:'
        if id == 10:
            return 'please select teacher of class'
        if id == 11:
            return 'please enter the seq id(0 for all):'


    @staticmethod
    def successMessage(id):
        if id == 0:
            return 'Student checkin_files Result updated Successfully ,new record : '
        if id == 1:
            return 'Student Records initialization Successful'
        if id == 2:
            return 'Sum Records initialization Successful'
        if id == 3:
            return 'Detail Records initialization Successful'
        if id == 4:
            return 'Files initialization Successful'
        if id == 5:
            return 'Detail Records updated Successfully'
        if id == 6:
            return "kick  previous checkin_files obj off Successfully"
        if id == 7:
            return "join in the check in list Successfully"
        if id == 8:
            return "check in  Successfully"
        if id == 9:
            return "Timer is out"
        if id == 10:
            return "Timer is start"


    @staticmethod
    def failedMessage(id):
        if id == 0:
            return 'Wrong (0):'+'Time window is closed'
        if id == 1:
            return 'Wrong (1): checkin_files type ,please try again'
        if id == 2:
            return 'Wrong (2):'+'due to current class is on check in,failed to open time window'
        if id == 3:
            return 'Wrong (3):'+'Please open it during class or 5 minutes before'
        if id == 4:
            return 'Wrong (4):'+ 'Wrong wechat id'
        if id == 5:
            return 'Wrong (5):'+ 'Wrong wechat id or no such check in obj'
        if id == 6:
            return 'Wrong (6):'+ 'please start check in first'
        if id == 7:
            return 'Wrong (7):'+ 'you have already launched a check in'

    @staticmethod
    def tipsMessage(id):
        if id == 0:
            return 'the check in list is empty!'
