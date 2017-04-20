import sys
import MySQLdb
import dbconn2
from mngo_dsn import dsn


################################################
# sql statement to add users to database
################################################
def insertUser(nm,email,password,year):
    username = email.split("@")[0]
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    print("before")
    curs.execute("INSERT into wellesley_people (nm,email,username,password,year)"+\
        "values (%s,%s,%s,%s,%s)",(nm,email,username,password,year))
    print("after")
    return True

################################################
# 
################################################
def insertAnecdote(conn,title,content,lat,lng,username):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    print("before")
    try:
        print("in try")
    	curs.execute("INSERT into anecdotes (title,content,lat,lng,username)"+ \
    		"values (%s,%s,%s,%s,%s)",(title,content,lat,lng,username))
        print("after")
    	return True
    except MySQLdb.Error:
        print("error")
    	return False

################################################
# 
################################################
def getAnecdotesByUser(conn,username):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("SELECT * from anecdotes where username=%s",(username,))
    return curs.fetchall()

################################################
# 
################################################
def getAllAnecdotes(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("SELECT * from anecdotes")
    return curs.fetchall()

################################################
# 
################################################
def checkCredentials(conn,username,password):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("SELECT count(*) as count from wellesley_people where username=%s and password=%s",(username,password))
    count = curs.fetchone()['count']
    return True if count == 1 else False

################################################
# 
################################################
# query for person in wellesley_people (upon login)
def getUserInfo(conn,username):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("SELECT * from wellesley_people where username=%s",(username,))
    return curs.fetchone()

################################################
# gets database connection
################################################
def getConn():
    dsn['db'] = 'mapdb_db' # the database we want to connect to
    conn = dbconn2.connect(dsn)
    return conn

