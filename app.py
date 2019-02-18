import numpy as np
import wave
import logging
import hashlib
from datetime import datetime

from database import Session, Eventlogs, Eventnames, Users, Musics, SQLiteHandler

def create_eventnames(funcs):
    session = Session()
    names =  session.query(Eventnames).all()
    if len(names) == 0:
        for func in funcs:
            session.add(Eventnames(event_name=func))
    session.commit()
    session.close()
    print('DONE: init db')

def login(data):
    session = Session()
    user = session.query(Users).filter_by(user_name=data['user_name']).all()
    session.close()
    user_id = -1
    password = hashlib.sha256(data['user_password'].encode()).hexdigest()
    if len(user) == 1:
        if user[0].user_password == password:
            msg = 'success'
            user_id = user[0].id
        else:
            msg = 'wrong password'
    else:
        msg = 'wrong username'
    return {'isFound': len(user), 'user_id': user_id, 'msg': msg}

def signup(data):
    name = data['user_name']
    user_id = -1
    session = Session()
    user = session.query(Users).filter_by(user_name=name).all()
    if len(user) == 0:
        user_id = session.query(Users).count() + 1
        session.add(Users(
            user_name=name,
            user_password=hashlib.sha256(data['user_password'].encode()).hexdigest(),
            created_at=datetime.now().isoformat(' ', 'seconds')
        ))
        session.commit()
        msg = 'succeeded to create an user account'
    else:
        msg = 'already exists'
    session.close()
    return {'user_id': user_id, 'msg': msg}

def logged_in(user_id):
    # TODO: write here for auto login
    if user_id == -1:
        return 0
    session = Session()
    result = session.query(Eventlogs).filter_by(user_id=user_id).all()
    event_name_logout = session.query(Eventnames).filter_by(event_name='logout').one().id
    session.close()
    if len(result) == 0:
        return 0
    elif result[-1].event_id == event_name_logout:
        return 0
    else:
        return 1

def music_list():
    session = Session()
    songs = session.query(Musics).all()
    session.close()
    result = []
    for song in songs:
        result.append([song.id, song.song_name, song.singer])
    return result

def add_music(name, singer):
    session = Session()
    song = session.query(Musics).filter_by(song_name=name, singer=singer).all()
    if len(song) != 0:
        print('another song found')
        return -1
    song_id = session.query(Musics).count() + 1
    session.add(Musics(
        song_name=name,
        singer=singer,
        created_at=datetime.now().isoformat(' ', 'seconds'),
    ))
    session.commit()
    session.close()
    return song_id

class WebSocketApp:
    def __init__(self):
        self.data = []
        self.counter = 0
        self.max_index = 0
    def upload(self, data):
        self.data.append((np.frombuffer(data, dtype='float32') * 32767).astype(np.int16))
        self.counter += 1
    def return_counter(self):
        return self.counter
    def close(self, data):
        v = np.array(self.data).flatten()
        with wave.Wave_write('hoge.wav') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(data['framerate'])
            wf.writeframes(v.tobytes('C'))

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
