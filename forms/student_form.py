from base_form import Form
from main_form import MainForm


class StudentForm(Form):

    name = 'student menu'

    def __init__(self):
        self.path = [MainForm.name, self.name]
        self.items = ['join check in', 'back']
        Form.__init__(self, self.path, self.items)

