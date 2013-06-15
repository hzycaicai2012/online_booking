#!/usr/bin/env python
#coding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+mysqldb://root:12345@localhost/online_booking', convert_unicode=True)
#engine = create_engine('sqlite:////home/hzycaicai/study/develop/online/tmp/test1.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
	import models
	Base.metadata.create_all(bind=engine)
