from __future__ import absolute_import, division, print_function, unicode_literals
import logging
from datetime import datetime
import os

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

__version__ = "0.1.0"

engine = create_engine('sqlite:///database.sqlite3', echo=False)
Base = declarative_base()

Session = sessionmaker(bind=engine)

class Eventlogs(Base):
	__tablename__ = 'eventlogs'
	id = Column('id', Integer, primary_key=True)
	asctime = Column('asctime', String)
	log_name = Column('log_name', String)
	levelno = Column('levelno', Integer)
	funcname = Column('funcname', String)
	log_message = Column('log_message', String)
	user_id = Column('user_id', Integer)
	event_id = Column('event_id', Integer)
	push = Column('push', String)
	result = Column('result', String)

	def __repr__(self):
		return '<Eventlogs(id=%s, asctime=%s, log_name=%s, levelno=%s, funcname=%s, log_message=%s, user_id=%s, event_id=%s, push=%s, result=%s, )>' \
			% (self.log_id, self.asctime, self.log_name, self.levelno, self.funcname, self.log_message, self.user_id, self.event_id, self.push, self.result)

class Users(Base):
	__tablename__ = 'users'
	id = Column('id', Integer, primary_key=True)
	user_name = Column('user_name', String)
	user_password = Column('user_password', String)
	created_at = Column('created_at', String)

	def __repr__(self):
		return '<Users(id=%s, user_name=%s, user_password=%s, created_at=%s, )>' \
			% (self.user_id, self.user_name, self.user_password, self.created_at)

class Event_log(Base):
	__tablename__ = 'event_log'
	id = Column('id', Integer, primary_key=True)
	event_name = Column('event_name', String)

	def __repr__(self):
		return '<Event_log(id=%s, event_name=%s, )>' \
			% (self.event_id, self.event_name)

class SQLiteHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        session = Session()
        session.commit()
        session.close()

    def _rec(self, record):
        record.asctime = datetime.now().isoformat(' ', 'seconds')
        if '@_@' in record.msg:
            i = record.msg.index('@_@')
            message = record.msg[:i]
            record.msg = record.msg[i+2:]
        else:
            message = record.msg
        if record.msg[0] != '@':
            record.user_id = 0
            record.event_id = 0
            record.push = ''
            record.result = ''
        else:
            recs = record.msg[1:].split(' ')
            record.user_id = int(recs[0])
            record.event_id = int(recs[1])
            record.push = recs[2]
            record.result = recs[3]
        record.msg = message
        return record

    def emit(self, record):
        sql = "INSERT INTO eventlogs (asctime, log_name, levelno, funcname, log_message, user_id, event_id, push, result) VALUES ('%(asctime)s', '%(name)s', '%(levelno)s', '%(funcName)s', '%(msg)s', '%(user_id)s', '%(event_id)s', '%(push)s', '%(result)s')"
        record = self._rec(record)
        session = Session()
        session.execute(sql % record.__dict__)
        session.commit()
        session.close()

if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = Session()
    session.add(Users(
        id=0,
        user_name='master',
        user_password='hogehoge',
        created_at=0,
    ))
    session.commit()
    session.close()