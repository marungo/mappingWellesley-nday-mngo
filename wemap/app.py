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

# Global variable to avoid hacking via entering username directly in URL
logged_in = False

# URL for map page for a logged in user
@app.route('/<username>', methods=['POST', 'GET'])
def map(username):
	if request.method=="POST":
		if request.form['submit'] == "Go To Your Profile":
			# print("user button")
			return redirect(url_for('user', username=username))
		else:
			lat = request.form['lat']
			lng = request.form['lng']
			title = request.form['title']
			content = request.form['content']
			conn = queries.getConn()
			worked = queries.insertAnecdote(conn,title,content,lat,lng,username)
	
	global logged_in	
	if not logged_in:
		flash("you need to log in!")
		return redirect(url_for('login'))
	conn = queries.getConn()
	anecdotes = queries.getAllAnecdotes(conn)
	return render_template('map.html', username=username, anecdotes=anecdotes)

# URL for login page
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
        	return redirect(url_for('map', username=username))
        else:
            flash("Sorry; incorrect")
            return render_template('login.html')
    return render_template('login.html')

@app.route('/user/<username>', methods=["GET", "POST"])
def user(username):
	if request.method=="POST":
		return redirect(url_for('map', username=username))
	
	global logged_in
	if not logged_in:
		flash("You need to log in!")
		return redirect(url_for('login'))
	conn = queries.getConn()
	anecdotes = queries.getAnecdotesByUser(conn, username)
	user = queries.getUserInfo(conn,username)
	return render_template('user.html', user=user, anecdotes=anecdotes)


if __name__ == '__main__':
	app.debug = True
	app.run('0.0.0.0', os.getuid())
	# app.run()
