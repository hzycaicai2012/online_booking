# -*- coding: utf-8 -*-
"""
	OnlineBooking app 
    :copyright: (c) 2013 by Hzy ZJU.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import with_statement
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import Flask, request, jsonify, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack, send_from_directory
from models import *
from database import *
from config import Config
from werkzeug import secure_filename

# create the  application
app = Flask(__name__)

#import the config
app.config.from_object(Config)

city_list = {
		'bj' : '北京',
		'sh' : '上海',
		'hz' : '杭州',
		'gz' : '广州',
		'sz' : '深圳',
		'cd' : '成都',
		'ny' : '纽约',
		'ld' : '伦敦'}

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
	hotel_info = db_session.query(Hotel).all()
	pre_order = {}
	if session.get('logged_in'):
		pre_order = db_session.query(Pre_order).filter_by(user_id = 1).all()
	#hotel_info = db_session.query(Hotel.id, Hotel.name, Hotel.lowest_price,Hotel.hotel_pic,Hotel.score).order_by(Hotel.name).all()
	return render_template('my.html', hotel_info=hotel_info, pre_order=pre_order)

@app.route('/sort_hotel')
def sort_hotel():
	#hotel_info = db_session.query(Hotel.id, Hotel.name, Hotel.lowest_price,Hotel.hotel_pic,Hotel.score).all()
	hotel_info = db_session.query(Hotel.id, Hotel.name, Hotel.lowest_price,Hotel.hotel_pic,Hotel.score).order_by(Hotel.name).all()
	return hotel_info

@app.route('/hotel')
def hotel():
	error = None
	hotel_info = db_session.query(Hotel.id, Hotel.name, Hotel.lowest_price,Hotel.hotel_pic,Hotel.score).all()
	room_info = {} 
	for hotel in hotel_info:
		room_info[hotel.id] = db_session.query(Room).filter_by(hotel_id=hotel.id).all()
	pre_order = {}
	if session.get('logged_in'):
		pre_order = db_session.query(Pre_order).filter_by(user_id = 1).all()
	return render_template('hotel.html',hotel_info=hotel_info, room_info = room_info, pre_order=pre_order)


@app.route('/hotel/add', methods=['GET','POST'])
def add_hotel():
	if not session.get('manager'):
		abort(401)
	if request.method == 'POST':
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
	return render_template('hotel_add.html')


@app.route('/get_hotel')
def get_hotel():
	city = request.args.get('city')
	if city == 'button-nav':
		hotel_info = db_session.query(Hotel).all()
	else:
		city = city_list[city]
		hotel_info = db_session.query(Hotel).filter_by(city=city).all()
	html = u'<tbody>'
	for info in hotel_info:
		html = html + u'<tr> <td width="20%"><img alt="140x140" src="'
		img = url_for('static', filename='img/'+info.name + '.jpg')
		html = html + img
		html = html + u'" class="img-round" /> </td>'
		html = html + u'<td width=57%><ol class="unstyled"> <li> <h4>'+ info.name + '<small>----星级</small> </h4> </li>'
		html = html + u'<li> <small>' + info.location +'</small> </li>'
		html = html + u'<li> <small>' + str(info.score) +'|评论数</small></li><li><small>最近评论</small></li></ol></td>'
		html = html + u'<td width="20%">	<div>' + str(info.lowest_price) + '元起！</div>'
		if session.get('manager'):
			url = url_for('update_hotel', hotel_id=info.id)
			html = html + u'<a href="' + url + '"><button class="btn btn-primary" type="button">更新</button></a>'
		else:
			url = url_for('hotel_detail', hotel_id=info.id)
			html = html + u'<a href="' + url + '"><button class="btn btn-primary" type="button">去看看</button></a>'
		html = html + u'</td> </tr>'
	html = html + u'</tbody>'
	print html
	return html 


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


@app.route('/hotel/search', methods=['POST'])
def search_hotel():
	error = None
	key = '%' + request.form['key'] + '%'
	hotel_info = db_session.query(Hotel).filter(Hotel.name.like(key)).all()
	room_info = {} 
	for hotel in hotel_info:
		room_info[hotel.id] = db_session.query(Room).filter_by(hotel_id=hotel.id).all()
	pre_order = {}
	if session.get('logged_in'):
		pre_order = db_session.query(Pre_order).filter_by(user_id = 1).all()

	return render_template('hotel.html',hotel_info=hotel_info, room_info = room_info, pre_order=pre_order)


@app.route('/hotel/<hotel_id>/add_room', methods=['POST'])
def add_room(hotel_id):
	if not session.get('manager'):
		abort(401)
	r = Room(hotel_id,
			request.form['room_type'],
			request.form['current_price'],
			request.form['discount'])
	db_session.add(r)
	db_session.commit()
	flash('New Room was posted successfully~~')
	return redirect(url_for('hotel_detail',hotel_id=hotel_id))

@app.route('/hotel/<hotel_id>/delete_room/<room_id>')
def delete_room(hotel_id, room_id):
	if not session.get('manager'):
		abort(401)
	db_session.query(Room).filter_by(id=room_id).delete()
	db_session.commit()
	flash('Room was deleted successfully~~')
	return redirect(url_for('hotel_detail',hotel_id=hotel_id))


@app.route('/hotel/book_room/<hotel_id>/<room_id>', methods=['POST'])
def book_room(hotel_id, room_id):
	order_id = "1-"+str(hotel_id)+"-"+str(room_id)
	b = Pre_order(order_id, 1,
				request.form['start_date'],
				request.form['end_date'])
	db_session.add(b)
	db_session.commit()
	hotel_detail = db_session.query(Hotel).filter_by(id=hotel_id).all()
	room_detail = db_session.query(Room).filter_by(hotel_id=hotel_id).all()
	pre_order = {}
	if session.get('logged_in'):
		pre_order = db_session.query(Pre_order).filter_by(user_id = 1).all()

	return render_template('hotel_detail.html', hotel_detail = hotel_detail,hotelid = hotel_id,room_detail=room_detail, pre_order=pre_order)

@app.route('/hotel/detail/<hotel_id>')
def hotel_detail(hotel_id):
	if hotel_id <= 0:
		abort(401)
	hotel_detail = db_session.query(Hotel).filter_by(id=hotel_id).all()
	room_detail = db_session.query(Room).filter_by(hotel_id=hotel_id).all()
	pre_order = {}
	if session.get('logged_in'):
		pre_order = db_session.query(Pre_order).filter_by(user_id = 1).all()

	return render_template('hotel_detail.html', hotel_detail = hotel_detail,hotelid = hotel_id,room_detail=room_detail, pre_order=pre_order)

@app.route('/flight')
def flight():
	error = None
	flight_info = db_session.query(Flight).all()
	pre_order = {}
	if session.get('logged_in'):
		pre_order = db_session.query(Pre_order).filter_by(user_id = 1).all()

	return render_template('flight.html',flight_info=flight_info, pre_order=pre_order)

@app.route('/flight/add', methods=['GET','POST'])
def add_flight():
	if not session.get('manager'):
		abort(401)
	if request.method == 'POST':
		non_stop = True
		if request.form['path']!="":
			non_stop = False
		f = Flight(request.form['company'],
				request.form['flight_num'],
				request.form['start_city'],
				request.form['stop_city'],
				request.form['start_time'],
				request.form['stop_time'],
				request.form['start_airport'],
				request.form['stop_airport'],
				request.form['path'],
				non_stop,	
				request.form['plane_type'])
		db_session.add(f)
		db_session.commit()
		flash('New Flight was posted successfully~~')
		return redirect(url_for('flight'))
	return render_template('flight_add.html')


@app.route('/flight/update/<flight_id>', methods=['GET','POST'])
def update_flight(flight_id):
	error = None
	if not session.get('manager'):
		return redirect(url_for('login'))

	flight_detail = db_session.query(Flight).filter_by(id=flight_id).all()
	if request.method == 'POST':
		if flight_id<=0:
			abort(401)
		non_stop = True
		if request.form['path']!="":
			non_stop = False
		f = db_session.query(Flight)
		f.filter(Flight.id==flight_id).update({
			Flight.company : request.form['company'],
			Flight.flight_num : request.form['flight_num'],
			Flight.start_city : request.form['start_city'],
			Flight.stop_city : request.form['stop_city'],
			Flight.start_time : request.form['start_time'],
			Flight.stop_time : request.form['stop_time'],
			Flight.start_airport : request.form['start_airport'],
			Flight.stop_airport : request.form['stop_airport'],
			Flight.path : request.form['path'],
			Flight.non_stop : non_stop,	
			Flight.plane_type : request.form['plane_type']})
		db_session.commit()
		flash('Flight was updated successfully~~')
		return redirect(url_for('flight'))

	return render_template('flight_update.html', flight_detail = flight_detail)

@app.route('/update/<blog_id>')
def update():
	error = None



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



if __name__ == '__main__':
    init_db()
    app.run()
