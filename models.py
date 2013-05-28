#!/usr/bin/env python
#coding=utf-8
from sqlalchemy import Table, Column, Integer, String, Float, Boolean, Text, Date, ForeignKey, MetaData
from sqlalchemy.orm import relationship, backref
from database import Base

class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	name = Column(String(50), unique=True)
	email = Column(String(120), unique=True)
	intro = Column(String(255), unique=True)

	def __init__(self, name = None, email = None, intro = None):
		self.name = name
		self.email = email
		self.intro = intro

	def __repr__(self):
		return '<User %r>' % (self.name)

class Blog(Base):
	__tablename__ = 'blog'
	id = Column(Integer, primary_key=True)
	title = Column(String(20), nullable=False)
	contents = Column(String)

	def __init__(self, title=None, contents=None):
		self.title = title
		self.contents = contents

	def __repr__(self):
		return '%r' % (self.title)

class Hotel(Base):
	__tablename__ = 'hotel'
	id = Column(Integer, primary_key=True)
	name = Column(String(20), nullable=False)
	city = Column(String(10), nullable=False)
	location = Column(String(100), nullable=False)
	telphone = Column(String(20))
	lowest_price = Column(Float(4), nullable=False)
	detail_info = Column(Text(500))
	hotel_pic = Column(String(50),nullable=False)
	star = Column(Integer, nullable=False,default=0)
	score = Column(Integer,nullable=False,default=0)
	rooms = relationship("Room", backref="hotel")

	def __init__(self,
			name=None,
			city=None,
			location=None,
			telphone=None,
			lowest_price=None,
			hotel_pic=None,
			detail_info=None,
			star=0,
			score=0):

		self.name=name
		self.city=city
		self.location=location
		self.telphone=telphone
		self.lowest_price=lowest_price
		self.hotel_pic=hotel_pic
		self.detail_info=detail_info
		self.star=star
		self.score=score

	def __repr__(self):
		return '%r' % (self.name)

class Room(Base):
	__tablename__ = 'room'
	id = Column(Integer, primary_key=True)
	hotel_id = Column(Integer, ForeignKey('hotel.id'), nullable=False)
	room_type = Column(String(20),nullable=False)
	capacity = Column(Integer, nullable=False, default=30)
	occupied = Column(Integer, nullable=False, default=0)
	current_price = Column(Float(4), nullable=False)
	discount = Column(Float(1), nullable=False)

	def __init__(self,
			hotel_id = None,
			room_type=None,
			current_price=None,
			discount=None,
			capacity=30,
			occupied=0):
		self.hotel_id=hotel_id
		self.room_type=room_type
		self.capacity = capacity
		self.occupied = occupied
		self.current_price=current_price
		self.discount=discount

	def __repr__(self):
		return '%r' % (self.room_type)


class Flight(Base):
	__tablename__ = 'flight'
	id = Column(Integer, primary_key=True)
	company = Column(String(30), nullable=False)
	flight_num = Column(String(30), nullable=False)
	start_city = Column(String(30), nullable=False)
	stop_city = Column(String(30), nullable=False)
	start_time = Column(String(30), nullable=False)
	stop_time = Column(String(30), nullable=False)
	start_airport = Column(String(30), nullable=False)
	stop_airport = Column(String(30), nullable=False)
	path = Column(String(40))
	non_stop = Column(Boolean,nullable=False,default=True)
	plane_type = Column(String(30),nullable=False)
	order_nums = Column(Integer,nullable=False,default=0)
	score  = Column(Integer,nullable=False,default=0)
	cabins = relationship("Cabin", backref="flight")

	def __init__(self,
			company=None,
			flight_id=None,
			start_city=None,
			stop_city=None,
			start_time=None,
			stop_time=None,
			start_airport=None,
			stop_airport=None,
			path=None,
			non_stop=True,
			plane_type=None,
			order_nums=0,
			score=0):

		self.company=company
		self.flight_id=flight_id
		self.start_city=start_city
		self.stop_city=stop_city
		self.start_time=start_time
		self.stop_time=stop_time
		self.start_airport=start_airport
		self.stop_airport=stop_airport
		self.path = path
		self.non_stop = non_stop
		self.plane_type = plane_type
		self.order_nums = order_nums
		self.score = score

	def __repr__(self):
		return '%r' % (self.company)

class Cabin(Base):
	__tablename__ = 'cabin'
	id = Column(Integer, primary_key=True)
	flight_id = Column(Integer, ForeignKey('flight.id'), nullable=False)
	cabin_type = Column(String(30),nullable=False)
	capacity = Column(Integer, nullable=False, default=30)
	occupied = Column(Integer, nullable=False, default=0)
	current_price = Column(Float(4), nullable=False)
	discount = Column(Float(1), nullable=False)

	def __init__(self,
			flight_id = None,
			cabin_type=None,
			current_price=None,
			discount=None,
			capacity=30,
			occupied=0):
		self.flight_id=flight_id
		self.cabin_type=cabin_type
		self.capacity = capacity
		self.occupied = occupied
		self.current_price=current_price
		self.discount=discount

	def __repr__(self):
		return '%r' % (self.room_type)


class Comment(Base):
	__tablename__ = 'comment'
	order_id = Column(Integer, primary_key=True, autoincrement=False)
	content = Column(Text,nullable=False)
	score = Column(Integer,nullable=False,default=5)

	def __init__(self,
			order_id = None,
			content=None,
			score=5):
		self.order_id=order_id
		self.content=content
		self.score = score 

	def __repr__(self):
		return '%r' % (self.order_id)

