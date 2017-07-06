#-*-coding:utf-8-*-

class Form():

    def __init__(self, path, items):
        self.path = path
        self.items = items

    def init_form(self):
        length = max([(len(i) + 2) for i in self.items]) + 36
        heights = 2 + len(self.items)
        index = '->'.join(self.path)

        left = '║                 '
        right = '                 ║'

        dict = {
            'above': '╔' + '═' * length + '╗',
            'bottom': '╚' + '═' * length + '╝',
            'blank': '║' + ' ' * length + '║',
            'index': index,
        }

        for i in range(0, len(self.items)):
            s = str(i + 1) + '.' + self.items[i]
            l = length + 6 - len(left) - len(right) - len(s)
            dict.update({str(i + 1): left + s + ' ' * l + right})
        print
        print dict['index']
        for i in range(0, heights):
            if i == 0:
                print dict['above'] + '\n' + dict['blank']
            elif i == heights - 1:
                print dict['bottom']
            else:
                print dict[str(i)] + '\n' + dict['blank']
        return self.choice()

    def choice(self):
        while True:
            choice = int(raw_input('your choice :'))
            if choice > int(len(self.items)) or choice < 1:
                print 'wrong input, try again!'
            else:
                return choice
