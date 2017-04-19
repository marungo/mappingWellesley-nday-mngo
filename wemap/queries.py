import sys
import MySQLdb
import dbconn2
from mngo_dsn import dsn
# insert into wellesley_people (upon signup)
# def addAccount(nm,email,password,year):

# THIS WORKS
def checkCredentials(conn,username,password):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("SELECT count(*) as count from wellesley_people where username=%s and password=%s",(username,password))
    count = curs.fetchone()['count']
    return True if count == 1 else False

# query for person in wellesley_people (upon login)

# insert anecdotes

################################################
# gets database connection
################################################
def getConn():
    dsn['db'] = 'mngo_db' # the database we want to connect to
    conn = dbconn2.connect(dsn)
    return conn