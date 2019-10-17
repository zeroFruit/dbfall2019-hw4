from userAcc import *
from DBconnection import *


def instructor_menu():

    menu_num = -1

    while menu_num != '0':
        print("\n\nWelcome %s" % user_acc.name)
        print("select instructor menu")
        print("1) Course Report")
        print("0) Quit")
        menu_num = input("Enter : ")

        switcher = {
            '0': quit_menu,
            '1': print_course_report
            
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

def print_course_report() :
    
    c = user_acc.conn.cursor()

    #교수가 가르친 가장 최근 학기의 교수아이디랑 같은 수업 이름 찾기
    c.execute("SELECT DISTINCT dept_name, course_id, sec_id, title, building, room_number,year,semester,time_slot_id\
                FROM course NATURAL JOIN teaches NATURAL JOIN section\
                WHERE teaches.ID = %s \
                AND teaches.year IN (SELECT MAX(year) FROM teaches WHERE ID = %s GROUP BY ID) AND teaches.semester = 'Fall'"%(user_acc.ID,user_acc.ID))
    
    title_fall = c.fetchall()

    c.execute("SELECT DISTINCT dept_name, course_id, sec_id, title, building, room_number,year,semester,time_slot_id\
                FROM course NATURAL JOIN teaches NATURAL JOIN section\
                WHERE teaches.ID = %s \
                AND teaches.year IN (SELECT MAX(year) FROM teaches WHERE ID = %s GROUP BY ID) AND teaches.semester = 'Spring'"%(user_acc.ID,user_acc.ID))

    title_spring = c.fetchall()

    if(title_fall) :
        data_season = title_fall
    else: data_season = title_spring

    # 수업 개수 구하기
    c.execute("SELECT COUNT(*) \
                FROM course NATURAL JOIN teaches NATURAL JOIN section \
                WHERE teaches.ID = %s \
                AND teaches.year IN (SELECT MAX(year) FROM teaches WHERE ID = %s GROUP BY ID) AND teaches.semester = 'Fall'"%(user_acc.ID,user_acc.ID))
    
    count_fall = c.fetchone()

    c.execute("SELECT COUNT(*) \
                FROM course NATURAL JOIN teaches NATURAL JOIN section\
                WHERE teaches.ID = %s \
                AND teaches.year IN (SELECT MAX(year) FROM teaches WHERE ID = %s GROUP BY ID) AND teaches.semester = 'Spring'"%(user_acc.ID,user_acc.ID))

    count_spring = c.fetchone()

    if(count_fall[0] != 0) :
        count_data = count_fall
    else: count_data = count_spring

    if(count_data[0] != 0): print("Course report -  %s  %s"%(data_season[0][6],data_season[0][7]))
    else: print("Course report - No Data")
    
   
    ## print loop
    for i in range(0,count_data[0]) :

        c.execute("SELECT day, start_hr, start_min, end_hr, end_min\
                FROM time_slot\
                WHERE time_slot.time_slot_id = '%s'"%(data_season[i][8]))

        timeslot = c.fetchall()    

        c.execute("SELECT COUNT(*)\
                FROM time_slot\
                WHERE time_slot.time_slot_id = '%s'"%(data_season[i][8]))

        count_timeslot = c.fetchone()

        
        if(count_timeslot[0] != 0) :
            time_string = timeslot[0][0]
            for temp in range(1,count_timeslot[0]):
                time_string = time_string + ", %s"%(timeslot[temp][0])
        
            time_string += " %s : %s - %s : %s"%(timeslot[0][1],timeslot[0][2],timeslot[0][3],timeslot[0][4])

        else: time_string = "No Data"

        print("%s-%s-%s   %s      [%s %s]  (%s)"%(data_season[i][0],data_season[i][1],data_season[i][2],data_season[i][3],data_season[i][4],data_season[i][5],time_string))
        print("ID        name       dept_name       grade")
        
        c.execute("SELECT ID, name, dept_name, grade, year, semester, course_id, sec_id \
                FROM student NATURAL JOIN takes\
                WHERE takes.course_id = %s\
                AND takes.sec_id = %s\
                AND takes.year = %s\
                AND takes.semester = '%s'"%(data_season[i][1],data_season[i][2],data_season[i][6],data_season[i][7]))
        
        student = c.fetchall()

        c.execute("SELECT COUNT(*)\
                FROM student NATURAL JOIN takes\
                WHERE takes.course_id = %s\
                AND takes.sec_id = %s\
                AND takes.year = %s\
                AND takes.semester = '%s'"%(data_season[i][1],data_season[i][2],data_season[i][6],data_season[i][7]))

        count_student = c.fetchone()

        for j in range(0,count_student[0]):
            print("%s      %s        %s       %s"%(student[j][0],student[j][1],student[j][2],student[j][3]))
        print() 

    # cursor 닫기
    c.close()

    return




def print_wrong():
    print("\nwrong menu number. ")
    return
