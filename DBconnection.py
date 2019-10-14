import MySQLdb
import conf


db_host = conf.DATABASE_CONFIG['host']
db_user = conf.DATABASE_CONFIG['user']
db_pw = conf.DATABASE_CONFIG['password']
db_name = conf.DATABASE_CONFIG['name']

connect_pool = []


def connectDB():
    connect = MySQLdb.connect(db_host, db_user, db_pw, db_name)
    return connect


def get_connect():
    global connect_pool
    if not connect_pool:
        connect_tmp = connectDB()
        connect_pool.append(connect_tmp)
    return connect_pool.pop()


def return_connect(conn):
    global connect_pool
    connect_pool.append(conn)
    return


def close_db(db):
    db.close()
    return
