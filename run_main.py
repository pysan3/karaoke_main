import responder
import sqlite3

import os
import sys
import io
import cgi
from random import randint

import app as backapp
import music as backmusic

api = responder.API(templates_dir='./dist', static_dir='./dist/static')
api.add_route(websocket=True)
logger = backapp.create_logger(__name__)
# logger.info(msg@_@event_id, user_id, push, result)

functions = [
    'index',
    'random_number',
    'loggedin',
    'login',
    'signup',
    'logout',
    'musiclist',
    'upload',
    'ws_upload',
    'load_music',
    'ws_sing'
]

@api.route('/')
async def index(req, resp):
    f_index = functions.index(sys._getframe().f_code.co_name)
    logger.info('@{0} {1} _ index.html'.format(0, f_index))
    resp.content = api.template('index.html')

@api.route('/api/login')
async def login(req, resp):
    f_index = functions.index(sys._getframe().f_code.co_name)
    user = await req.media()
    # {'user_name': '', 'user_password': ''}
    result = backapp.login(user)
    # {'user_id': number, 'msg': ''}
    logger.info('{0}@_@{1} {2} {3} {4}'.format(
        result['msg'], f_index, result['user_id'], user['user_name'], (result['user_id'] != -1)
    ))
    resp.media = result

@api.route('/api/logout')
async def logout(req, resp):
    f_index = functions.index(sys._getframe().f_code.co_name)
    user_id = await req.text
    logger.info('{0}@_@{1} {2} {3} {4}'.format(
        'logout', f_index, user_id, 'logout request', 1
    ))
    resp.text = '1'

@api.route('/api/loggedin/{user_id}')
async def loggedin(req, resp, *, user_id):
    f_index = functions.index(sys._getframe().f_code.co_name)
    result = backapp.logged_in(int(user_id))
    # result = 1 / 0
    logger.info('{0}@_@{1} {2} {3} {4}'.format(
        '' if result else 'not ' + 'logged in', f_index, user_id, user_id, result
    ))
    resp.text = str(result)

@api.route('/api/signup')
async def signup(req, resp):
    f_index = functions.index(sys._getframe().f_code.co_name)
    user = await req.media()
    # {'user_name': '', 'user_password': ''}
    result = backapp.signup(user)
    # {'user_id':user_id, 'msg':msg}
    logger.info('{0}@_@{1} {2} {3} {4}'.format(
        result['msg'], f_index, result['user_id'], user['user_name'], (result['user_id'] != -1)
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

@api.route('/api/upload')
async def upload(req, resp):
    f_index = functions.index(sys._getframe().f_code.co_name)
    data = cgi.FieldStorage(fp=io.BytesIO(await req.content), environ={'REQUEST_METHOD': 'POST'}, headers=req.headers)
    song = {d.name:d.value for d in data.list}
    # {'user_id':number, 'song_name':name, 'singer':singer, 'music':data}
    song_id = backapp.add_music(song['song_name'], song['singer'])
    if song_id != -1:
        backmusic.upload(song_id, song['music'])
        logger.info('{0}@_@{1} {2} {3} {4}'.format(
            'music upload', f_index, song['user_id'], song_id, 1
        ))
    resp.media = {'song_id':song_id}

@api.route('/audio/load_music/{req_id}')
async def load_music(req, resp, *, req_id):
    f_index = functions.index(sys._getframe().f_code.co_name)
    user_id = req_id.split('_')[0]
    song_id = req_id.split('_')[1]
    result = backmusic.load_music(song_id)
    logger.info('{0}@_@{1} {2} {3} {4}'.format(
        'music_request', f_index, user_id, song_id, 1
    ))
    resp.content = result

@api.route('/ws/sing', websocket=True)
async def ws_sing(ws):
    f_index = functions.index(sys._getframe().f_code.co_name)
    ws_handler = backapp.WebSocketApp()
    await ws.accept()
    data = await ws.receive_json()
    while True:
        try:
            ws_handler.upload(await ws.receive_bytes())
        except:
            ws_handler.close(data)
            break
    logger.info('{0}@_@{1} {2} {3} {4}'.format(
        'ws connection completed', f_index, data['user_id'], '_', '_'
    ))

@api.route('/api/random')
def random_number(req, resp):
    f_index = functions.index(sys._getframe().f_code.co_name)
    result = {'randomNumber': randint(1, 100)}
    logger.info('{0}@_@{1} {2} {3} {4}'.format(
        'randomNumber request', f_index, 0, '', result['randomNumber']
    ))
    resp.media = result

if __name__ == '__main__':
    backapp.create_eventnames(functions)
    api.run()
