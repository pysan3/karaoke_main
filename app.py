import logging
import server
from database import SQLiteHandler

def create_logger(filename):
    logger = logging.getLogger(filename)
    fmt = '%(name)s %(levelno)s %(funcName)s %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=fmt)
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    sqlite_handler = SQLiteHandler()
    sqlite_handler.setLevel(logging.INFO)
    logger.addHandler(sqlite_handler)
    logger.propagate = False
    return logger

def login(data):
    name = data['user_name']
    password = data['user_password']
    return server.login(name, password)

def check_database():
    server.add_users()
    user_dataset = server.return_users()
    for user in user_dataset:
        print(user.id, user.user_name, user.user_password, user.created_at)

def debug():
    check_database()

if __name__ == '__main__':
    debug()