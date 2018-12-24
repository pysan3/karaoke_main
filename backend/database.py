from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine('sqlite:///database.sqlite3', echo=True)
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

if __name__ == '__main__':
	Base.metadata.create_all(engine)