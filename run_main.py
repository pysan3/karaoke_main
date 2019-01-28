import responder
import sqlite3
import sys
import json
from random import randint
import time

import app as backapp

api = responder.API(templates_dir='./dist', static_dir='./dist/static')
logger = backapp.create_logger(__name__)
# logger.info(msg@_@event_id, user_id, push, result)

functions = [
    'index',
    'random_number',
    'loggedin',
    'login',
    'signup',
    'musiclist',
    'ws_upload',
]
backapp.create_eventnames(functions)

@api.route('/')
async def index(req, resp):
    f_index = functions.index(sys._getframe().f_code.co_name)
    logger.info('@{0} {1} _ index.html'.format(0, f_index))
    resp.content = api.template('index.html')

@api.route('/api/login')
async def login(req, resp):
    f_index = functions.index(sys._getframe().f_code.co_name)
    user = await req.media()
    # {'user_name': 'hoge', 'user_password': 'fuga'}
    result = backapp.login(user)
    # {'isFound': 1 / 0, 'user_id': number, 'msg': 'hoge'}
    logger.info('{0}@_@{1} {2} {3} {4}'.format(
        result['msg'], f_index, result['user_id'], user['user_name'], result['isFound']
    ))
    resp.media = result

@api.route('/api/loggedin')
async def loggedin(req, resp):
    f_index = functions.index(sys._getframe().f_code.co_name)
    user = await req.media()
    # {'user_id': number}
    result = backapp.logged_in(user)
    # {'isLoggedin': 1 / 0}
    logger.info('{0}@_@{1} {2} {3} {4}'.format(
        '' if result['isLoggedin'] else 'not ' + 'logged in', f_index, user['user_id'], user['user_id'], result['isLoggedin']
    ))
    resp.media = result

@api.route('/api/signup')
async def signup(req, resp):
    f_index = functions.index(sys._getframe().f_code.co_name)
    user = await req.media()
    # {'user_name': 'hoge', 'user_password': 'fuga'}
    result = backapp.signup(user)
    # {'succeed': 1 / 0, 'user_id':user_id, 'msg':msg}
    logger.info('{0}@_@{1} {2} {3} {4}'.format(
        result['msg'], f_index, result['user_id'], user['user_name'], result['succeed']
    ))
    resp.media = result

@api.route('/api/musiclist')
async def musiclist(req, resp):
    f_index = functions.index(sys._getframe().f_code.co_name)
    user_id = await req.media()
    result = backapp.music_list()
    # {'id':number, 'name':'song_name', 'singer':'singer_name'}
    logger.info('{0}@_@{1} {2} {3} {4}'.format(
        'success', f_index, user_id['user_id'], '', 'list of musics'
    ))
    resp.media = result

# @api.route('/api/upload')
# async def upload(req, resp):
#     f_index = functions.index(sys._getframe().f_code.co_name)
#     song = await req.media()
#     # {'user_id':number, 'song_name':name, 'singer':singer}
#     print('sent data:', song)
#     result = backapp.add_music(song['song_name'], song['singer'])
#     logger.info('{0}@_@{1} {2} {3} {4}'.format(
#         'music upload', f_index, song['user_id'], song['song_name'], '1'
#     ))
#     resp.media = {'success':result}

@api.route('/ws/upload')
async def ws_upload(ws):
    f_index = functions.index(sys._getframe().f_code.co_name)
    ws_audio = backapp.WebSocketHandler()
    await ws.accept()
    while True:
        song = await ws.receive_json()
        ws_audio.upload(song)
    await ws.send_json({'success':1})
    await ws.close()
    logger.info('{0}@_@{1} {2} {3} {4}'.format(
        'music upload', f_index, song['user_id'], song['song_name'], '1'
    ))
    ws_audio.close('hoge')

@api.route('/api/random')
def random_number(req, resp):
    f_index = functions.index(sys._getframe().f_code.co_name)
    result = {'randomNumber': randint(1, 100)}
    logger.info('{0}@_@{1} {2} {3} {4}'.format(
        'randomNumber request', f_index, 0, '', result['randomNumber']
    ))
    resp.media = result

if __name__ == '__main__':
    api.run(debug=True)
