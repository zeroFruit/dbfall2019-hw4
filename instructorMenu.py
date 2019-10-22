from userAcc import *
from DBconnection import *


def instructor_menu():

    menu_num = -1

    while menu_num != '0':
        print("\n\nWelcome %s" % user_acc.name)
        print("select instructor menu")

        print("1) Course report")
        print("2) Advisee report")
        print("0) Quit")

        menu_num = input("Enter : ")

        switcher = {
            '0': quit_menu,
            '1': course_report,
            '2': advisee_report,
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


def course_report():
    pass


def advisee_report():

    c = user_acc.conn.cursor()

    ## instructor 가 advise 한 학생의 id를 advisor 에서 찾는다.
    c.execute("SELECT s_ID "
              "FROM advisor "
              "WHERE i_ID = \"%s\" "
              % user_acc.ID)

    s_IDs = c.fetchall()

    ## 찾은 학생들의 ID에 해당하는 정보를 출력한다.

    if s_IDs is None:
        print("\nAdvised Student not exist")
        pass

    print("\n%10s\t%15s\t%20s\t%10s"
          % ("ID", "name", "dept_name", "tot_cred"))

    for s_id in s_IDs:

        c.execute("SELECT * "
                  "FROM student "
                  "WHERE ID = \"%s\" "
                  % s_id)
        
        std_data = c.fetchone()

        std_id, std_name, std_dept, std_cred = std_data

        print("%10s\t%15s\t%20s\t%10s"
                % (std_id, std_name, std_dept, std_cred))


    ## 사용한 cursor  닫기
    c.close()

    pass


def print_wrong():
    print("\nwrong menu number. ")
    return
