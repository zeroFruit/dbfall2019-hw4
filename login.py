from userAcc import *
from DBconnection import *
from studentMenu import *
from instructorMenu import *


def login():

    print('Welcome')

    while user_acc.conn is None:

        print("\nPlease sign in")

        ID = input("%-10s:" % "ID")
        name = input("%-10s:" % "Name")

        auth(ID, name)

    switcher = {
        0: student_menu,
        1: instructor_menu
    }

    role_menu = switcher.get(user_acc.role)

    role_menu()


def auth(ID, name):

    user_connect = get_connect()
    curs = user_connect.cursor()

    # base sql
    base_sql = f"SELECT * FROM %s WHERE ID = \"{ID}\" AND name = \"{name}\""

    # student table에 해당 ID와 name을 가진 row가 있는지 확인
    is_student = curs.execute(base_sql % "student")

    if is_student:
        # user account의 attribute들을 설정한다. (student로)
        user_acc.set_attrs(ID, name, 0, user_connect)
        return
    else:
        # instructor table에 해당 ID와 name을 가진 row가 있는지 확인
        is_instructor = curs.execute(base_sql % "instructor")

        if is_instructor:
            # user account의 attribute들을 설정한다. (instructor로)
            user_acc.set_attrs(ID, name, 1, user_connect)
            return
        else:
            # student, instructor 모두가 아닐 때
            print("\nWrong authentication.")

            # user가 사용하던 connection 반납
            return_connect(user_connect)
            return
