from userAcc import *
from DBconnection import *


def student_menu():

    # 메뉴 UI 출력 및 동작에 해당하는 함수 출력
    menu_num = -1

    while menu_num != '0':
        print("\n\nWelcome %s" % user_acc.name)
        print("Please select student menu")
        print("1) Student Report")
        print("2) View Time Table")
        print("0) Quit")
        menu_num = input("Enter : ")

        switcher = {
            '0': quit_menu,
            '1': print_stud_report,
            '2': print_time_table
        }

        selected_func = switcher.get(menu_num, print_wrong)

        selected_func()

    return


def print_time_table():

    c = user_acc.conn.cursor()

    # 해당 학생이 수강한 year, semester 쌍을 시간 순서대로 모두 출력
    c.execute("SELECT year, semester "
              "FROM takes "
              "WHERE ID = \"%s\" "
              "GROUP BY year, semester "
              "ORDER BY year DESC, semester"
              % user_acc.ID)

    results = c.fetchall()

    print("Please select semester to view")

    i = 0
    for result in results:
        i = i + 1
        print("%2s) %s %s" % (i, result[0], result[1]))

    semester_num = int(input())

    year, semester = results[semester_num - 1]

    print("\nTime Table\n")
    print("%10s\t%40s\t%15s\t%10s\t%10s"
          % ("course_id", "title", "day", "start_time", "end_time"))

    c.execute("select course_id, title, day, start_hr, start_min, end_hr, end_min "
              "from takes natural join course natural join section natural join time_slot "
              "where ID = %s and semester = \"%s\" and year = \"%s\""
              % (user_acc.ID, semester, year))

    course_times = c.fetchall()

    for course_time in course_times:
        course_id, title, day, start_hr, start_min, end_hr, end_min = course_time
        start_time = "%02d : %02d" % (start_hr, start_min)
        end_time = "%02d : %02d" % (end_hr, end_min)
        print("%10s\t%40s\t%15s\t%10s\t%10s"
              % (course_id, title, day, start_time, end_time))

    # 사용한 cursor  닫기
    c.close()

    return


def get_sortkey(semesterDict, x):
    semester = semesterDict[x[3]]
    year = int(x[4])
    return year * 10 + semester
    
def process(data):
    if len(data) == 0:
        return data
    splitBySemester = []
    same_semester = [data[0]]
    first_lecture = data[0]
    prev_semester = first_lecture[3]
    prev_year = first_lecture[4]
    for lecture in data[1:]:
        _, course_id, _, semester, year, grade, title, dept_name, credit = lecture
        if semester == prev_semester and year == prev_year:
            same_semester.append(lecture)
        else:
            splitBySemester.append(same_semester)
            same_semester = [lecture]
        prev_semester = semester
        prev_year = year
    splitBySemester.append(same_semester)
    return splitBySemester
            

def print_stud_report():

    semesterDict = {"Spring" : 1, "Summer" : 2, "Fall" : 3, "Winter" : 4}
    gpaDict = {"A+": 4.3, "A": 4.0, "A-": 3.7, "B+": 3.3, "B" : 3.0, "B-":2.7, 
               "C+": 2.3, "C": 2.0, "C-":1.7, "D+": 1.3, "D": 1.0, "D-" : 0.7, "F": 0}
    c = user_acc.conn.cursor()
    c.execute("SELECT * FROM student WHERE ID = \"%s\" and name = \"%s\""%(user_acc.ID, user_acc.name))

    data = c.fetchone()
    print("You are a member of %s"%data[2])
    
    totalCreditIsZero = True if data[3] == None else False
    if totalCreditIsZero:
        totalCredit = "0"
        print("You have taken total %s credit\n"%totalCredit)
        c.close()
        return 
    
    print("You have taken total %s credit\n"%data[3])
    print("Semester report")
    
    sql = "select * from takes as T natural join course as C where T.ID in (select ID from student where name = '{}');".format(user_acc.name)
    c.execute(sql)
    
    data = list(c.fetchall())
    # 출력 데이터 : ID, course_id, sec_id, semester, year, grade, title, dept_name, credit
    data.sort(key=lambda x: get_sortkey(semesterDict, x))

    coursesBySem = process(data)[::-1]

    # DONE : grade Null 처리 
    # Done : Tot_cred Null 처리 
    gradeIsNull = False
    for courseInSem in coursesBySem:
        total_gpa = 0
        total_credit = 0
        for course in courseInSem:
            course_id, _, _, semester, year, grade, title, dept_name, credit = course
            if grade == None:
                gradeIsNull = True
                break
            total_gpa += gpaDict[grade] * int(credit)
            total_credit += int(credit)
        if not gradeIsNull:
            avg_gpa = total_gpa / total_credit
            print("\n%s\t%s\tGPA : %.5f"%(year, semester, avg_gpa))
        else:
            print("\n%s\t%s\tGPA : "%(year, semester))
        for course in courseInSem:
            course_id, _, _, semester, year, grade, title, dept_name, credit = course
            print("%10s\t%40s\t%15s\t%8s\t%8s" %("course_id", "title", "debt_name", "credit", "grade"))
            if grade == None:
                print("%10s\t%40s\t%15s\t%8s\t" %(course_id, title, dept_name, credit))
            else:
                print("%10s\t%40s\t%15s\t%8s\t%8s" %(course_id, title, dept_name, credit, grade))
            gradeIsNull = False

    c.close()

    return


def print_course_qual():

    c = user_acc.conn.cursor()

    while(True):
        print("\nCheck Course Qualification")
        course_info = input("Enter course ID or Title (Enter q to quit)")

        if(course_info == "q" or course_info == "Q"):
            break

        # Select course_id from course where title = input

        # If course id가 없다면
        #   input은 title이 아니라 course_id 일 수도 있다.
        #   Select title from course where course_id = input
        #   if title이 없다면
        #       해당 course는 존재하지 않는다 출력
        #       return
        #   else: #input이 course_id일 때
        #       course_id = input
        #       course_title = title
        # else: #input이 title일 때
        #   course_id = course_id
        #   course_title = input


def quit_menu():
    global user_acc # global 변수 write할 때는 명시 필요

    # user가 사용하던 connection 반납
    return_connect(user_acc.conn)

    del user_acc

    return


def print_wrong():
    print("\nwrong menu number. ")
    return

