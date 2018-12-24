#pylint: skip-file
from database import *
from datetime import datetime

def login(name, password):
    session = Session()
    user = session.query(Users).filter(Users.user_name==name).all()
    session.close()
    if len(user) == 1:
        if user.user_password == password:
            return 'true'
        else:
            return 'false'
    elif len(user) == 0:
        return 'no users'
    else:
        return 'too many users'

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
