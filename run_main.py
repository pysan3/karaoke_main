# pylint: skip-file

# WARNING : THIS CODE DOES NOT WORK

import responder
import sqlite3
import sys
from random import randint

import app as backapp

api = responder.API(templates_dir='./dist', static_dir='./dist/static')
logger = backapp.create_logger(__name__)

@api.route('/')
async def index(req, resp):
    reqest = req.media
    responce = api.template('index.html')
    # result = makeResult([reqest['user_id'], 'index', 0, 'index.html'])
    print('got another request')
    logger.debug('test')
    logger.info('@{0} {1} 0 index.html'.format(0, 1))
    resp.content = responce

@api.route('/api/login')
async def login(req, resp):
    isLogin = backapp.login(req.media())
    result = {'isLogin':isLogin}
    resp.media = result

@api.route('/api/random')
def random_number(req, resp):
    result = {
        'randomNumber': randint(1, 100)
    }
    resp.media = result


if __name__ == '__main__':
    api.run(debug=True)
