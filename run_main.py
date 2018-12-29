import responder
import sqlite3
import sys
from random import randint

import app as backapp

api = responder.API(templates_dir='./dist', static_dir='./dist/static')
logger = backapp.create_logger(__name__)

@api.route('/')
async def index(req, resp):
    logger.info('@{0} {1} 0 index.html'.format(0, 1))
    resp.content = api.template('index.html')

@api.route('/api/login')
async def login(req, resp):
    user = req.media()
    # {'user_name': 'hoge'}
    result = backapp.login(user)
    # {'isFound': 1 / 0, 'user_id': number, 'result': 1 / 0}
    if result['isFound'] == 1:
        logger.info('@{0} {1} {2} {3}'.format(result['user_id'], 2, user['user_name'], result['result']))
    else:
        logger.warning('no user exists@_@{0} {1} {2} {3}'.format(result['user_id'], 2, user['user_name'], result['result']))
    resp.media = result

@api.route('/api/loggedin')
async def loggedin(req, resp):
    user = req.media()
    # {'user_name': 'hoge'}
    isLogged_in = backapp.logged_in(user)
    # {'isFound': 1 / 0, 'user_id': number, 'result': 1 / 0}
    if isLogged_in['isFound'] == 'true':
        logger.info('@{0} {1} {2} {3}'.format(isLogged_in['user_id'], 2, user['user_name'], isLogged_in['result']))
    else:
        logger.warning('no user exists@_@{0} {1} {2} {3}'.format(isLogged_in['user_id'], 2, user['user_name'], isLogged_in['result']))
    resp.media = isLogged_in

@api.route('/api/signin')
async def signin(req, resp):
    user = req.media()
    # {'user_name': 'hoge', 'user_password': 'fuga'}
    result = backapp.signin(user)
    logger.info('{0}@_@{1} {2} {3}'.format(result['msg'], result['user_id'], user['user_name'], result['succeed']))
    resp.media = result

@api.route('/api/random')
def random_number(req, resp):
    result = {
        'randomNumber': randint(1, 100)
    }
    resp.media = result


if __name__ == '__main__':
    api.run(debug=True)
