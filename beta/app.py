#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_cas import CAS
from werkzeug.security import generate_password_hash, check_password_hash

import os
import sys
print(sys.getdefaultencoding())
# my own set of mysql query and statement functions
import queries

app = Flask(__name__)
app.secret_key = '39tsfkajie' # for flashing

# URL for WeMap: Mapping Wellesley Connections homepage
@app.route('/home/', methods=["GET", "POST"])
def home():
	if request.method == 'POST':
		if request.form['submit'] == "Login":
			return redirect(url_for('login'))
		if request.form['submit'] == "Sign Up":
			return redirect(url_for('signup'))
	return render_template('home.html')

# URL for login page
@app.route('/login/', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
    	if request.form['submit'] == 'login':
	        username = request.form['username']
	        password = request.form['password']
	        conn = queries.getConn()
	        if (username == "") or (password == ""):
	        	flash("Please enter your username and password!")
	        	return render_template('login.html')
	        elif queries.checkCredentials(conn,username,password):
	        	session['username'] = request.form['username']
	        	print(session.keys())
	        	return redirect(url_for('map', username=username))
	        else:
	            flash("Sorry; incorrect")
	            return render_template('login.html')
    return render_template('login.html')

# URL for signup page
@app.route('/signup/', methods=["GET", "POST"])
def signup():
	if request.method == 'POST':

		name = request.form['name']
		year = request.form['year']
		email = request.form['email']
		password = request.form['password']
		verify = request.form['verify']

		if "@wellesley.edu" not in email:
			flash('Email must be a valid Wellesley Email')
			return render_template('signup.html')

		username = email.split('@')[0]
		conn = queries.getConn()
		response = queries.addUser(conn,name,email,year,password,verify)
		if response == 0:
			flash('Username is taken. Either you already signed up or that is not your correct email.')
		elif response == 2:
			flash('Your passwords did not match. Try again.')
		else:
			# flash('welcome,'+ name+'!')
			session['username'] = username
			return redirect(url_for('user',username=username))
	return render_template('signup.html')

# URL for map page for a logged in user
@app.route('/<username>', methods=['POST', 'GET'])
def map(username):
	conn = queries.getConn()
	if request.method=="POST":
		if request.form['submit'] == "Go To Your Profile":
			# print("user button")
			return redirect(url_for('user', username=username))
		elif request.form['submit'] == 'add marker':
			lat = request.form['lat']
			lng = request.form['lng']
			title = request.form['title']
			content = request.form['content']
			try:
				anonymous = int(request.form['anon'])
			except:
				anonymous = 0

			info = [lat,lng,title,content];
			if "" in info:
				flash("please select a location, give a title and write your anecdote!");
			else:
				worked = queries.insertAnecdote(conn,title,content,lat,lng,username,anonymous)
		elif request.form['submit'] == 'filter anecdotes':
			content = request.form['content']
			print(content)
			if request.form['filtertype'] == 'username':
				print('reached username')
				filtered_anecdotes = queries.getAnecdotesByUser(conn, content)
				return render_template('map.html', username=username, anecdotes=filtered_anecdotes)
			elif request.form['filtertype'] == 'keyword':
				print('reached keyword')
				filtered_anecdotes = queries.getAnecdotesByKeyword(conn, content)
				return render_template('map.html', username=username, anecdotes=filtered_anecdotes)
	if 'username' not in session:
		flash("You need to log in!")
		return redirect(url_for('login'))
	anecdotes = queries.getAllAnecdotes(conn)
	return render_template('map.html', username=username, anecdotes=anecdotes)

# URL for user profile page
@app.route('/user/<username>', methods=["GET", "POST"])
def user(username):
	conn = queries.getConn()
	if request.method=="POST":
		if request.form['submit'] == 'Go To Map':
			return redirect(url_for('map', username=username))
		elif request.form['submit'] == 'Logout':
			session.pop('username', None)
			return redirect(url_for('home'))
		elif request.form['submit'] == 'Go to Profile':
			return redirect(url_for('user',username=username))
		elif request.form['submit'] == "Delete your anecdote":
			aid = request.form['aid']
			queries.deleteAnecdote(conn,aid)
		elif request.form['submit'] == 'update anecdote':
			title = request.form['title']
			content = request.form['content']
			user = request.form['username']
			aid = request.form['aid']
			try:
				anonymous = request.form['anon']
			except:
				anonymous = 0
			queries.updateAnecdote(conn,aid,title,content,user,anonymous)
	if 'username' not in session:
		flash("You need to log in!")
		return redirect(url_for('login'))
	print(username != session['username'])
	logged_in = username == session['username']
	anecdotes = queries.getAnecdotesByUser(conn, username)
	user = queries.getUserInfo(conn,username)
	return render_template('user.html', user=user, anecdotes=anecdotes, logged_in=logged_in)


if __name__ == '__main__':
	app.debug = True
	app.run('0.0.0.0', os.getuid())
	# app.run()
