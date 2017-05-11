# WeMap: Mapping Wellesley Connections
# Authors: MR Ngo and Naomi Day

import sys
import MySQLdb
import dbconn2
from mngo_dsn import dsn
from werkzeug.security import generate_password_hash, check_password_hash

################################################
# Add users to database. Name, email, password,
# year provided. Email must have @wellesley.edu,
# and is assumed to be a valid Wellesley address
# if formatted that way.
################################################
def insertUser(conn,nm,email,password,year):
    username = email.split("@")[0]
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("INSERT into wellesley_people (nm,email,username,password,yr)"+
        "values (%s,%s,%s,%s,%s)",(nm,email,username,password,year))

################################################
# Insert anecdote entered on map into database.
# Anecdote title, content, location (lat/long
# coordinates), and username are provided, as
# well as whether or not the user elected to
# have the anecdote displayed anonymously. All
# anecdotes in database are associated with a
# username.
################################################
def insertAnecdote(conn,title,content,lat,lng,username,anonymous):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    try:
    	curs.execute("INSERT into anecdotes (title,content,lat,lng,username,anonymous)"+
    		"values (%s,%s,%s,%s,%s,%s)",(title,content,lat,lng,username,anonymous))
        print (username)
    except MySQLdb.Error:
        print("error")

################################################
# Get all anecdotes where search input matches
# anything in any titles or content of anecdotes.
################################################
def getAnecdotesByKeyword(conn, search):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    search = "%"+consearchtent+"%"
    curs.execute("SELECT * from anecdotes where search like %s or title like %s",(search,search))
    return curs.fetchall()

################################################
# Get all anecdotes belonging to a certain user
# (username provided).
################################################
def getAnecdotesByUser(conn,username):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("SELECT * from anecdotes where username=%s",(username,))
    return curs.fetchall()

################################################
# Get all anecdotes that currently exist in the
# database.
################################################
def getAllAnecdotes(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("SELECT * from anecdotes")
    return curs.fetchall()

################################################
# Check that username and password correctly
# match a user in our database.
################################################
def checkCredentials(conn,username,password):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("SELECT password from wellesley_people where username=%s",(username,))
    return check_password_hash(curs.fetchone()['password'],password)

################################################
# Get all user information from database, given
# a username. This happens when logging in.
################################################
def getUserInfo(conn,username):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("SELECT * from wellesley_people where username=%s",(username,))
    return curs.fetchone()


################################################
# Upon sign up, check if a user already exists in 
# database. If they do not, add them to the
# database and log them in with the provided
# credentials so long as the password and verify
# password are the same.
# Return type:
# 0: username is taken
# 1: success
# 2: passwords do not match
################################################
# query for person in wellesley_people (upon login)
def addUser(conn,name,email,year,password,verify):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("SELECT count(*) as count from wellesley_people where email=%s",(email,))
    if curs.fetchone()['count'] > 0:
        # must tell them username is taken
        return 0
    else:
        if password == verify:
            hashed_password = generate_password_hash(password)
            insertUser(conn,name,email,hashed_password,year)
            return 1
        return 2

################################################
# Update an anecdote (identified by the aid) with
# title, content, author, and whether or not it
# displays anonymously. Called even if no fields
# are modified.
################################################
def updateAnecdote(conn,aid,title,content,author,anonymous):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('UPDATE anecdotes set title=%s,content=%s,username=%s,anonymous=%s where aid=%s',
        (title,content,author,anonymous,aid))

################################################
# Delete an anecdote (identified by the aid).
# Currently does not verify that user intended
# to delete anecdote.
################################################
def deleteAnecdote(conn,aid):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("DELETE from anecdotes where aid=%s", (aid,))
    print ("deleted from anecdotes aid " + aid)

################################################
# Gets database connection.
################################################
def getConn():
    dsn['db'] = 'mapdb_db' # the database we want to connect to
    conn = dbconn2.connect(dsn)
    return conn

