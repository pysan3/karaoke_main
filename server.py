#pylint: skip-file
from datetime import datetime
from database import *

def eventnames(funcs):
    session = Session()
    names =  session.query(Eventnames).all()
    if len(names) == 0:
        for func in funcs:
            session.add(Eventnames(event_name=func))
    session.commit()
    session.close()

def login(name, password):
    session = Session()
    user = session.query(Users).filter_by(user_name=name).all()
    session.close()
    isFound = 0
    user_id = -1
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

def signup(name, password):
    session = Session()
    user = session.query(Users).filter_by(user_name=name).one_or_none()
    session.close()
    succeed = 0
    user_id = -1
    if len(name) == 0:
        msg = 'user name too short'
    elif user == None:
        add_users(name, password)
        succeed = 1
        user_id = session.query(Users).filter_by(user_name=name).one().id
        msg = 'succeeded to create an user account'
    else:
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
    result = session.query(Eventnames).all()
    for data in result:
        print(data.id, data.event_name)
    print('done')
    session.close()

if __name__ == '__main__':
    main()
