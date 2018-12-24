import logging
import sqliteHandler

def create_logger(filename):
    logger = logging.getLogger(filename)
    fmt = '%(name)s %(levelno)s %(funcName)s %(message)s %(user_id)s %(event_id)s %(push)s %(result)s'
    logging.basicConfig(level=logging.DEBUG, format=fmt)
    logger.setLevel(logging.DEBUG)
    sqlite_handler = sqliteHandler.SQLiteHandler()
    sqlite_handler.setLevel(logging.DEBUG)
    logger.addHandler(sqlite_handler)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    logger.propagate = False
    return logger