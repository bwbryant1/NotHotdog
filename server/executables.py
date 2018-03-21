import MySQLdb as mdb

def make_sql():

    con = mdb.connect('127.0.0.1','brandon','DBpass','keycards',port=9006)
    return con
