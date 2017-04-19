# WeMap: Mapping Wellesley Connections
# Authors: MR Ngo and Naomi Day

import sys
import MySQLdb
import dbconn2
from mngo_dsn import dsn


################################################
# Add users to database
################################################
def insertUser(nm,email,password,year):
	username = email.split("@")[0]
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	try:
		curs.execute("INSERT into wellesley_people (nm,email,username,password,year)"+\
			"values (%s,%s,%s,%s,%s)",(nm,email,username,password,year))
		return True
	except MySQLdb.Error:
		return False

################################################
# Insert anecdote entered on map into database
################################################
def insertAnecdote(conn,title,content,lat,lng,pid):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    try:
    	curs.execute("INSERT into anecdotes (title,content,lat,lng,pid)"+ \
    		"values (%s,%s,%s,%s,%s)",(title,content,lat,lng,pid))
    	return True
    except MySQLdb.Error:
    	return False

################################################
# Get all anecdotes belonging to a certain user
################################################
def getAnecdotes(conn,pid):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("SELECT * from anecdotes where pid=%s",(pid,))
    return curs.fetchall()

################################################
# Check that username and password match a user in our database
################################################
def checkCredentials(conn,username,password):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("SELECT count(*) as count from wellesley_people where username=%s and password=%s",(username,password))
    count = curs.fetchone()['count']
    return True if count == 1 else False

################################################
# Upon login, get all user info from database
################################################
# query for person in wellesley_people (upon login)
def getUserInfo(conn,username):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("SELECT * from wellesley_people where username=%s",(username,))
    return curs.fetchone()

################################################
# Gets database connection
################################################
def getConn():
    dsn['db'] = 'mapdb_db' # the database we want to connect to
    conn = dbconn2.connect(dsn)
    return conn

