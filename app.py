import numpy as np
import wave
import logging
import server
import music
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
    sqlite_handler.setLevel(logging.DEBUG)
    logger.addHandler(sqlite_handler)
    logger.propagate = False
    return logger

def create_eventnames(funcs):
    server.eventnames(funcs)
    print('DONE: init db')

def login(data):
    name = data['user_name']
    password = data['user_password']
    return server.login(name, password)

def signup(data):
    name = data['user_name']
    password = data['user_password']
    return server.signup(name, password)

def logged_in(data):
    return {'result': 0}

def music_list():
    return server.music_list()

def add_music(name, singer):
    return server.addMusic(name, singer)

def music_data(song_id, data):
    return music.upload(song_id, data)

def load_music(song_id):
    return music.load_music(song_id)

class WebSocketApp:
    def __init__(self):
        self.data = []
        self.counter = 0
    def upload(self, data):
        self.data.append(np.frombuffer(data, dtype='float32'))
        self.counter += 1
    def return_counter(self):
        return self.counter
    def close(self):
        # print('end data : ', end='')
        # print(self.data)
        print(self.counter)
        # v = np.array(self.data)
        # v.flatten()
        # arr = (v * 32767).astype(np.int16)
        # with wave.Wave_write('hoge.wav') as wf:
        #     wf.setnchannels(1)
        #     wf.setsampwidth(2)
        #     wf.setframerate(48000)
        #     wf.writeframes(arr.tobytes('C'))
        # self.data.clear()

def check_database():
    server.add_users('takuto', '000')
    user_dataset = server.return_users()
    for user in user_dataset:
        print(user.id, user.user_name, user.user_password, user.created_at)

def debug():
    check_database()

if __name__ == '__main__':
    debug()
