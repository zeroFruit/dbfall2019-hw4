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
    pass


def print_wrong():
    print("\nwrong menu number. ")
    return
