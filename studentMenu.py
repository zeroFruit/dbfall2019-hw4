from userAcc import *
from DBconnection import *


grades_to_point = {
    'A+': 4.3,
    'A' : 4,
    'A-': 3.7,
    'B+': 3.3,
    'B' : 3,
    'B-': 2.7,
    'C+': 2.3,
    'C' : 2,
    'C-': 1.7,
    'D+': 1.3,
    'D' : 1,
    'D-': 0.7,
    'F' : 0
}

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


def quit_menu():
    global user_acc # global 변수 write할 때는 명시 필요

    # user가 사용하던 connection 반납
    return_connect(user_acc.conn)

    del user_acc

    return


def print_stud_report():

    c = user_acc.conn.cursor()
    c.execute("SELECT * "
              "FROM student "
              "WHERE ID = \"%s\" AND name = \"%s\""
              % (user_acc.ID, user_acc.name))

    data = c.fetchone()

    print("You are a member of %s" % data[2])
    print("You have taken total %s credits\n" % data[3])
    print("Semester report\n")

    # 해당 학생이 수강한 year, semester 쌍을 시간 순서대로 모두 출력
    c.execute("SELECT year, semester "
              "FROM takes "
              "WHERE ID = \"%s\" "
              "GROUP BY year, semester "
              "ORDER BY year, semester DESC"
              % user_acc.ID)

    results = c.fetchall()

    for result in results:
        year, semester = result

        c.execute("SELECT grade, credits "
                  "FROM takes NATURAL JOIN course "
                  "WHERE takes.ID = \"%s\" AND takes.semester = \"%s\" AND takes.year = \"%s\""
                  % (user_acc.ID, semester, year))

        courses_part = c.fetchall()

        grades, credit = list(zip(*courses_part))

        gps = []

        # TODO: GPA가 null인 경우 핸들링 필요
        ind = 0
        for grade in grades:
            for i in range(int(credit[ind])):
                gps.append(grades_to_point[grade.strip()])
            ind = ind + 1

        print("\n%s\t%s\tGPA : %f" % (year, semester, float(sum(gps) / len(gps))))

        c.execute("SELECT course_id, title, dept_name, credits, grade "
                  "FROM takes NATURAL JOIN course "
                  "WHERE takes.ID = \"%s\" AND takes.semester = \"%s\" AND takes.year = \"%s\""
                  % (user_acc.ID, semester, year))

        courses_all = c.fetchall()

        print("%10s\t%40s\t%15s\t%8s\t%8s"
              % ("course_id", "title", "debt_name", "credits", "grade"))
        for course in courses_all:
            course_id, title, debt_name, credits, grade = course
            print("%10s\t%40s\t%15s\t%8s\t%8s"
                  % (course_id, title, debt_name, credits, grade))

    # cursor 닫기
    c.close()

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


def print_wrong():
    print("\nWrong menu number. ")
    return
