# coding=utf-8
#
from fileimport.import_student import ImportStudentInfo
from fileimport.import_teacher import ImportTeacherInfo
from fileimport.import_course import ImportCourseInfo


if __name__ == '__main__':
    # 待导入教师信息文件
    new_file = '../external/teacherInfo.csv'
    # 目标文件
    orig_file = '../internal/teacherInfo.csv'
    # 实例化
    teacherInfo = ImportTeacherInfo()
    # 调用方法
    teacherInfo.file_import(new_file, orig_file)

    # 待导入学生信息文件
    new_file = '../external/studentInfo.csv'
    # # 目标文件
    orig_file = '../internal/studentInfo.csv'
    # # 实例化
    studentInfo = ImportStudentInfo()
    #
    studentInfo.file_import(new_file, orig_file)

    # # 待导入课程信息文件
    new_file = '../external/courseProgress.csv'
    # # 目标文件
    orig_file = '../internal/courseInfo.csv'
    # # 实例化
    CourseInfo = ImportCourseInfo()
    # # 调用方法
    CourseInfo.file_import(new_file, orig_file)
