#!/usr/bin/env python
#coding=utf-8
from sqlalchemy import Table, Column, Integer, String, Float, Text, Date, ForeignKey, MetaData
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
	room_type
	capacity
	occupied
	current_price = Column(Float(4), nullable=False)
	discount = Column(Float(1), nullable=False)

	def __init__(self,
			hotel_id = None,
			room_type=None,
			current_price=None,
			origin_price=None,
			discount=None,
			end_time=None):
		self.hotel_id=hotel_id
		self.room_type=room_type
		self.current_price=current_price
		self.origin_price=origin_price
		self.discount=discount
		self.end_time=end_time

	def __repr__(self):
		return '%r' % (self.room_type)


