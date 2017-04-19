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

@app.route('/', methods=['POST', 'GET'])
def base(username):
	print(username)
	# info = {}
	# if request.method=="post":
	# 	info['title'] = request.form['title']
	# 	info['contents'] = request.form['contents']
	return render_template('map.html')

@app.route('/login/', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
	    # Dealing with POST
	    # try:
        user = request.form['username']
        passwd = request.form['password']
        conn = queries.getConn()
        correct = queries.checkCredentials(conn,user,passwd)
        if correct:
        	# return redirect(url_for('user', username=user))
        	return redirect(url_for('base', username=user))
        else:
            flash("Sorry; incorrect")
            return render_template('login.html')
	    # except Exception as err:
	    #     print('Got this in /login/: ',err)
	    #     flash("Sorry, some kind of error occurred")
	    #     return render_template('login.html')
    return render_template('login.html')

@app.route('/user/<username>')
def user(username):
    return render_template('userpage.html', username=username)

if __name__ == '__main__':
	app.debug = True
	# app.run('0.0.0.0', os.getuid())
	app.run()
