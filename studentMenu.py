from userAcc import *
from DBconnection import *


def student_menu():

    menu_num = -1

    while menu_num != '0':
        print("\n\nWelcome %s" % user_acc.name)
        print("Please select student menu")
        print("1) Student Report")
        print("2) Check Course Qualification")
        print("3) View Time Table")
        print("0) Quit")
        menu_num = input("Enter : ")

        switcher = {
            '0': quit_menu,
            '1': print_stud_report,
            '2': print_course_qual,
            '3': print_time_table
        }

        selected_func = switcher.get(menu_num, print_wrong)

        selected_func()

    return


def print_stud_report():

    c = user_acc.conn.cursor()
    c.execute("SELECT * FROM student WHERE ID = \"%s\" and name = \"%s\"" % (user_acc.ID, user_acc.name))

    data = c.fetchone()

    print("You are a member of %s" % data[2])
    print("You have taken total %s credit\n" % data[3])
    print("Semester report\n")

    # 평점 구하는 과정
    # 수강한 학기, 연도 정보 모두 가져오기(distinct로 중복계산 방지)
    # takes table에서 사용자가 다닌 year, semester 쌍을 최근 순서로 가져온다.
    # For year, semester 쌍들에 대해서:
    #   takes, course table을 natural join하여 각 수업의 credit과 사용자가 받은 grade를 얻는다.
    #
    # grade, credit 정보 cursor에서 받아오기
    #   (grade1, credit1), (grade2, credit2) ... 을 (grade1, grade2, ...), (credit1, credit2, ...) 로 만든다.
    #   Zip을 이용하여 grades, credit list를 생성한다.
    #   For grade in grades:
    #       gp_to_float함수를 이용하여 gps list에 append

    #   print("\n%s\t%s\tGPA : %d"%(year, semester, sum(gps)/len(gps)))

    #   과목들 정보 출력
    #   print("%10s\t%40s\t%15s\t%8s\t%8s"
    #   %("course_id", "title", "debt_name", "credit", "grade"))
    # (grade1, credit1), (grade2, credit2) ... 을 (grade1, grade2, ...), (credit1, credit2, ...) 로 만든다.
    #   course, takes를 natural join하여 해당 semester, year에 수강한 강의 정보들을 만듬
    #   for course info in course_infos:
    #       위 출력 형식대로 course_id, title, dept_name, credit, grade를 줄 맞춰 출력

    # cursor 닫기
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


def print_time_table():

    c = user_acc.conn.cursor()

    # user가 수강한 year, semester 정보 받아오기
    # Takes table을 이용하여 user가 수강한 year, semester쌍을 최근 순서로 받아오기 (distinct로 중복계산 방지)

    print("\nTime Table\n")
    print("%10s\t%40s\t%15s\t%10s\t%10s" % ("course_id", "title", "day", "start_time", "end_time"))

    # user가 수강한 year, semester중 가장 최근 year, semester를 이용하여
    # time table 만들기
    # Takes, course, section, time_slot 을 natural join하여 사용자가 수강한 강의의 course_id, title과 그 강의의 시작과 끝 시간을 받아온다.
    # For course_time in course_times:
    #   위 형식에 맞춰 course_id, title, day, start_time, end_time 출력

    # 사용한 cursor  닫기
    c.close()

    return


def print_wrong():
    print("\nWrong menu number. ")
    return
