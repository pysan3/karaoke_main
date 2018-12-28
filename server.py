#pylint: skip-file
from datetime import datetime
from database import *

def login(name, password):
    session = Session()
    user = session.query(Users).filter(Users.user_name==name).all()
    session.close()
    isFound = 0
    user_id = 0
    msg = ''
    if len(user) == 1:
        if user.user_password == password:
            user_id = user.id
            isFound = 1
        else:
            msg = 'wrong password'
    elif len(user) == 0:
        msg = 'no users'
    else:
        msg = 'too many users'

def signin(name, password):
    pass

def add_users():
    session = Session()
    session.add(Users(
        user_name='Takuto',
        user_password='000',
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
