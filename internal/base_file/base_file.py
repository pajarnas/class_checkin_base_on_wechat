import csv


class BaseFile:
    columns = []

    def __init__(self,name):
        self.name = name

    def write_file(self, data,way='wb'):
        try:
            with open(self.name, way) as csv_file:
                FIEDLS = self.columns
                writer = csv.DictWriter(csv_file, fieldnames=FIEDLS)
                if way == 'wb':
                    writer.writerow(dict(zip(FIEDLS, FIEDLS)))
                for line in data:
                    writer.writerow(line)
                csv_file.close()

        except IOError:

            print "File open error : " + self.name + "\nplease check the filename"
            exit(-1)

    @staticmethod
    def read_file(filename, way='rb'):
        try:
            with open(filename, way) as csv_file:
                reader = csv.DictReader(csv_file)
                data = []
                for info in reader:
                    data.append(info)
                csv_file.close()
                return data
        except IOError:
            print "File open error : " + filename + "\nplease check the filename"
            exit(-1)


class SeqFile(BaseFile):
    columns = ['TeacherID','CourseID','SeqID','Time']

    def __init__(self, name='../seq.csv'):
        BaseFile.__init__(self, name)


class DetailFile(BaseFile):
    columns = ['StuID','checkinTime','ProofPath','checkinType','IsSuc','checkinResult']

    def __init__(self,name):
        BaseFile.__init__(self,name)


class SumFile(BaseFile):
    columns =['StuID']

    def __init__(self,name):
        BaseFile.__init__(self,name)


class StudentFile(BaseFile):
    columns = ['StuID', 'StuName', 'ClassID', 'WeChatID', 'FeaturePath']

    def __init__(self,name='../studentInfo.csv'):
        BaseFile.__init__(self,name)


class TeacherFile(BaseFile):
    columns = ["TeacherID", "TeacherName", "WeChatID"]

    def __init__(self,name='../teacherInfo.csv'):
        BaseFile.__init__(self,name)


class CourseFile(BaseFile):
    columns = ['CourseID', 'CourseName', 'TeacherID', 'ClassNums']

    def __init__(self,name='../courseInfo.csv'):
        BaseFile.__init__(self,name)


