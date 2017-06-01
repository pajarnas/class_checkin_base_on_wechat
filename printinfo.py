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
            return 'sorry,you are not in random checkin in list'
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


    @staticmethod
    def successMessage(id):
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
            return "kick  previous checkin obj off Successfully"
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
            return 'Wrong (1): checkin type ,please try again'
        if id == 2:
            return 'Wrong (2):'+'due to current class is on check in,failed to open time window'
        if id == 3:
            return 'Wrong (3):'+'Please open it during class or 5 minutes before'

    @staticmethod
    def tipsMessage(id):
        if id == 0:
            return 'the check in list is empty!'


