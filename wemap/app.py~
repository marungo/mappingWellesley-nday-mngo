# hwk6: MR Ngo
from __future__ import print_function
from flask import Flask, render_template, redirect, url_for, request, flash
# from flask_googlemaps import GoogleMaps
import os
import sys
# my own set of mysql query and statement functions
import queries

app = Flask(__name__)
app.secret_key = '39tsfkajie' # for flashing
# GoogleMaps(app, key='AIzaSyA-nT9fP4I7GrFPu_J-V-5ajx1Esns2aNk')

logged_in = False

@app.route('/<username>', methods=['POST', 'GET'])
def base(username):
	print(username)
	# info = {}
	# if request.method=="post":
	# 	info['title'] = request.form['title']
	# 	info['contents'] = request.form['contents']
	return render_template('map.html',username=username)

@app.route('/login/', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        passwd = request.form['password']
        conn = queries.getConn()
        correct = queries.checkCredentials(conn,username,passwd)
        if correct:
        	global logged_in
        	logged_in = True
        	return redirect(url_for('base', username=username))
        else:
            flash("Sorry; incorrect")
            return render_template('login.html')
    return render_template('login.html')

@app.route('/user/<username>')
def user(username):
	global logged_in
	if logged_in:
		conn = queries.getConn()
		user = queries.getUserInfo(conn,username)
		anecdotes = queries.getAnecdotes(conn, user['pid'])
		return render_template('user.html', user=user, anecdotes=anecdotes)
	flash("You need to login!")
	return redirect(url_for('login'))

if __name__ == '__main__':
	app.debug = True
	app.run('0.0.0.0', os.getuid())
	# app.run()
