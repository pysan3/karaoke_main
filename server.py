#pylint: skip-file
from datetime import datetime
from database import *


def login(name, password):
    session = Session()
    user = session.query(Users).filter_by(user_name=name).all()
    session.close()
    isFound = 0
    user_id = 0
    msg = ''
    if len(user) == 1:
        if user[0].user_password == password:
            user_id = user[0].id
            isFound = 1
            msg = 'success'
        else:
            msg = 'wrong password'
    elif len(user) == 0:
        msg = 'no users'
    else:
        msg = 'too many users'
    return {'isFound': isFound, 'user_id': user_id, 'msg': msg}


def signin(name, password):
    session = Session()
    user = session.query(Users).filter_by(user_name=name).one_or_none()
    session.close()
    if user == None:
        add_users(name, password)
        succeed = 1
        user_id = session.query(Users).filter_by(user_name=name).one().id
        msg = 'succeed create user account'
    else:
        succeed = 0
        user_id = 0
        msg = 'already exists'
    return {'succeed': succeed, 'user_id': user_id, 'msg': msg}


def add_users(name, password):
    session = Session()
    session.add(Users(
        user_name=name,
        user_password=password,
        created_at=datetime.now().isoformat(' ', 'seconds'),
    ))
    session.commit()
    session.close()


def return_users():
    session = Session()
    result = session.query(Users)
    session.close()
    return result


def main():
    session = Session()
    result = session.query(Event_log).all()
    for data in result:
        print(data.log_id, data.event_id)
    print('done')
    session.close()


if __name__ == '__main__':
    main()
