#-*-coding:utf-8-*-
from base_form import Form



class MainForm(Form):

    name = 'main menu'
    path = [name]

    def __init__(self):
        self.items = ['student login', 'teacher login', 'exit']
        Form.__init__(self, self.path, self.items)


if __name__ == '__main__':
    c = MainForm()
    c.init_form()