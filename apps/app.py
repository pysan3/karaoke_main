import numpy as np
import logging
import hashlib
from datetime import datetime

from apps.database import Session, Eventlogs, Eventnames, Users, Musics, Hsh, SQLiteHandler

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
    if len(result) == 0 or result[-1].event_id == event_name_logout:
        return 0
    else:
        return 1

def music_list():
    session = Session()
    songs = session.query(Musics).all()
    session.close()
    result = []
    for song in songs:
        result.append([song.id, song.song_title, song.singer])
    return result

def isExist(name, singer):
    session = Session()
    song = session.query(Musics).filter_by(song_title=name, singer=singer).all()
    session.close()
    return len(song) != 0

def add_music(name, singer):
    session = Session()
    song_id = session.query(Musics).count() + 1
    session.add(Musics(
        song_title=name,
        singer=singer,
        created_at=datetime.now().isoformat(' ', 'seconds'),
    ))
    session.commit()
    session.close()
    return song_id

def upload_hash(song_id, hash_table):
    # TODO: format table?
    session = Session()
    session.add(Hsh(
        song_id=song_id,
        hsh_data=hash_table
    ))
    session.commit()
    session.close()

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

def init_db():
    session = Session()
    session.add(Users(
        user_name='master',
        user_password='password',
        created_at=datetime.now().isoformat(' ', 'seconds'),
    ))
    session.add(Musics(
        song_title='wonder stella',
        singer='fhana',
        created_at=datetime.now().isoformat(' ', 'seconds'),
    ))
    session.commit()
    session.close()