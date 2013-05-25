#!/usr/bin/env python
#coding=utf-8
# configuration

class Config(object):
	DATABASE = '/tmp/flaskr.db'
	DEBUG = True
	SECRET_KEY = 'development key'
	USERNAME = 'hzy'
	PASSWORD = '12345'
	MANAGER = 'root'
	MANAGER_PWD = 'root'
	UPLOAD_FOLDER = '/home/hzycaicai/study/develop/online/static/img/'
	ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


class ProductionConfig(Config):
	DEBUG = False
