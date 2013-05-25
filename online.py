# -*- coding: utf-8 -*-
"""
	OnlineBooking app 
    :copyright: (c) 2013 by Hzy ZJU.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import with_statement
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack, send_from_directory
from models import *
from database import *
from config import Config
from werkzeug import secure_filename

# create the  application
app = Flask(__name__)

#import the config
app.config.from_object(Config)


#heck if an extension is valid
def allowed_file(filename):
	return '.' in filename and \
			filename.rsplit('.', 1)[1] in Config.ALLOWED_EXTENSIONS


#Closes the database again at the end of the request.
@app.teardown_request
def shutdown_session(exception=None):
	db_session.remove()


@app.route('/')
def index():
	hotel_info = db_session.query(Hotel.id, Hotel.name, Hotel.lowest_price,Hotel.hotel_pic,Hotel.score).all()
	return render_template('index.html', hotel_info=hotel_info)


@app.route('/hotel/add', methods=['POST'])
def add_hotel():
	if not session.get('manager'):
		abort(401)
	file = request.files['hotel_pic']
	filename = request.form['name']+"."+file.filename.rsplit('.', 1)[1]
	if file and allowed_file(file.filename):
		file.save(os.path.join(Config.UPLOAD_FOLDER, filename))
	h = Hotel(request.form['name'],
			request.form['city'],
			request.form['location'],
			request.form['telphone'],
			request.form['lowest_price'],
			filename,
			request.form['detail'])
	db_session.add(h)
	db_session.commit()
	flash('New Hotel was posted successfully~~')
	return redirect(url_for('hotel'))


@app.route('/hotel/update/<hotel_id>', methods=['GET','POST'])
def update_hotel(hotel_id):
	error = None
	if not session.get('manager'):
		return redirect(url_for('login'))

	hotel_detail = db_session.query(Hotel).filter_by(id=hotel_id).all()
	if request.method == 'POST':
		if hotel_id<=0:
			abort(401)
		h = db_session.query(Hotel)
		h.filter(Hotel.id==hotel_id).update({
			Hotel.name : request.form['name'],
			Hotel.city : request.form['city'],
			Hotel.location : request.form['location'],
			Hotel.telphone : request.form['telphone'],
			Hotel.lowest_price : request.form['lowest_price'],
			Hotel.hotel_pic :  request.form['hotel_pic'],
			Hotel.detail_info : request.form['detail']})
		db_session.commit()
		flash('Hotel was updated successfully~~')
		return redirect(url_for('hotel'))

	return render_template('hotel_update.html', hotel_detail = hotel_detail)


#@app.route('/search/hotel/<hotel_name>', methods=['GET','POST'])
#def search_hotel(hotel_name):
#	error = None
#	if request.method == 'POST':
#		if len(hotel_name)>30:
#			error = ('The search key is too long~~')
#			return render_template('search_error.html',error)
#		h = db_session.query(Hotel)
#		h.filter(Hotel.name
#
@app.route('/update/<blog_id>')
def update():
	error = None

@app.route('/hotel/detail/<hotel_id>')
def hotel_detail(hotel_id):
	if hotel_id <= 0:
		abort(401)
	hotel_detail = db_session.query(Hotel).filter_by(id=hotel_id).all()
	return render_template('hotel_detail.html', hotel_detail = hotel_detail)


@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] == Config.USERNAME and request.form['password'] == Config.PASSWORD:
			session['user'] = True
			session['username'] = request.form['username'] 
		elif request.form['username'] == Config.MANAGER and request.form['password'] == Config.MANAGER_PWD:
			session['manager'] = True 
			session['managername'] = request.form['username'] 
		else:
			error = 'Invalid password'

		if error == None: 
			session['logged_in'] = True
			flash('Welcome, you are logged in~~')
			return redirect(url_for('index'))
		else:
			return render_template('login.html', error=error)
	return render_template('login.html', error=error)


@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	if session.get('user'):
		session.pop('username', None)
		session.pop('user', None)
	if session.get('manager'):
		session.pop('manager', None)
		session.pop('managername', None)
	flash('You were logged out')
	return redirect(url_for('index'))

@app.route('/hotel')
def hotel():
	error = None
	hotel_info = db_session.query(Hotel.id, Hotel.name, Hotel.lowest_price,Hotel.hotel_pic,Hotel.score).all()
	return render_template('hotel.html',hotel_info=hotel_info)


if __name__ == '__main__':
    init_db()
    app.run()
