# hwk6: MR Ngo
from __future__ import print_function
from flask import Flask, render_template, redirect, url_for, request, flash
# from flask_googlemaps import GoogleMaps
import os
import sys
# my own set of mysql query and statement functions

app = Flask(__name__)
app.secret_key = '39tsfkajie' # for flashing
# GoogleMaps(app, key='AIzaSyA-nT9fP4I7GrFPu_J-V-5ajx1Esns2aNk')

@app.route('/', methods=['POST', 'GET'])
def base():
	return render_template('map.html')

if __name__ == '__main__':
	app.debug = True
	# app.run('0.0.0.0', os.getuid())
	app.run()

