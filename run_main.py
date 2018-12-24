# pylint: skip-file

# WARNING : THIS CODE DOES NOT WORK

import responder
import sqlite3
import sys

import backend.app as backapp

api = responder.API(debug=True, templates_dir='./dist', static_dir='./dist/static')
logger = backapp.createLogger(__name__)

#
"""
db_name = './database.sqlite3'

def return_event_id(event_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    while True:
        cur.execute('search * from event_log where event_name=?', event_name)
        fetch_all = cur.fetchall()
        if len(fetch_all) == 1:
            break
        elif len(fetch_all) > 1:
            print('too many event_log')
            cur.execute('select * from event_log')
            for row in cur.fetchall():
                print(row)
            sys.exit()
        cur.execute('insert into event_log (event_name) values (?)', event_name)
    return fetch_all[0]
"""

def makeResult(features):
    if type(features[1]) is not int:
        features[1] = return_event_id(features[1])
    label = ['user_id', 'event_id', 'push', 'result']
    return {i:'null' if j==0 else j for i, j in zip(label, features)}

@api.route('/')
async def index(req, resp):
    reqest = req.media
    responce = api.template('index.html')
    result = makeResult([reqest['user_id'], 'index', 0, 'index.html'])
    logger.info('null', extra=result)
    resp.content = responce

@api.route('/api/login')
async def login(req, resp):
    isLogin = backapp.login(req.media())
    result = {'isLogin':isLogin}
    resp.media = result

if __name__ == '__main__':
    api.run()