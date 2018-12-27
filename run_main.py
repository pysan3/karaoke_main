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
    isLogin = backapp.login(req.media())
    result = {
        'isLogin': isLogin
    }
    resp.media = result

@api.route('/api/loggedin')
async def loggedin(req, resq):
    user = req.media()
    # {'user_name': 'hoge'}
    isLogged_in = backapp.logged_in(user)
    # {'user_found': 'true / false', 'user_id': 'number', 'result': 'true / false'}
    if isLogged_in['user_found'] == 'true':
        logger.info('@{0} {1} {2} {3}'.format(isLogged_in['user_id'], 2, user['user_name'], isLogged_in['result']))
    else:
        logger.warning('@{0} {1} {2} {3} {4}'.format('no user exists@_@', isLogged_in['user_id'], 2, user['user_name'], isLogged_in['result']))
    return isLogged_in

@api.route('/api/random')
def random_number(req, resp):
    result = {
        'randomNumber': randint(1, 100)
    }
    resp.media = result


if __name__ == '__main__':
    api.run(debug=True)
