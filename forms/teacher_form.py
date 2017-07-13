from base_form import Form
from main_form import MainForm


class TeacherForm(Form):

    name = 'teacher menu'

    def __init__(self):
        self.path = [MainForm.name, self.name]
        self.items = ['start check in', 'update check in detail', 'history',  'progress','back']
        Form.__init__(self, self.path, self.items)


class StartForm(Form):

    name = 'start menu'

    def __init__(self):
        self.path = [MainForm.name,TeacherForm.name,self.name]
        self.items = ['start auto check in', 'start manual check in','start random check in', 'back']
        Form.__init__(self, self.path, self.items)


class UpdateForm(Form):

    name = 'update menu'

    def __init__(self):
        self.path = [MainForm.name, TeacherForm.name, self.name]
        self.items = ['update once check in','back']
        Form.__init__(self, self.path, self.items)


class HistoryForm(Form):

    name = 'history'

    def __init__(self):
        self.path = [MainForm.name,TeacherForm.name,self.name]
        self.items = ['browse sum', 'browse detail file','browse once check in','back']
        Form.__init__(self, self.path, self.items)



class ProgressForm(Form):

    name = 'progess'

    def __init__(self):
        self.path = [MainForm.name, TeacherForm.name,self.name]
        self.items = ['Attendance', 'Absence','Real-time Detail Records','Real-time Check in list','back']
        Form.__init__(self, self.path, self.items)

if __name__ == '__main__':
    a = TeacherForm()
    a.init_form()
    c = StartForm()
    c.init_form()
    d = HistoryForm()
    d.init_form()
    e = UpdateForm()
    e.init_form()
    b = ProgressForm()
    b.init_form()