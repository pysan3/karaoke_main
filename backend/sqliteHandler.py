from __future__ import absolute_import, division, print_function, unicode_literals
import logging
from datetime import datetime
from database import Session

__version__ = "0.1.0"

class SQLiteHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        session = Session()
        session.commit()

    def emit(self, record):
        sql = 'insert into eventlogs (asctime, log_name, levelno, funcName, log_message, user_id, event_id, push, result) values (?,?,?,?,?,?,?,?,?)'
        event = [datetime.now()] + record.msg.split(' ')
        session = Session()
        session.execute(sql, event)
        session.commit()
        session.close()