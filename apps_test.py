import os
import sys
from glob import glob
from datetime import datetime

from run_main import functions
import apps.app as backapp
from apps.database import Base, engine, Session, Eventnames

def create_new_database():
    audio_list = glob('./audio/wav/[0-9]*.wav')
    for audio in audio_list:
        os.remove(audio)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    backapp.init_db()

def create_eventnames():
    session = Session()
    names =  session.query(Eventnames).all()
    for func in functions:
        if func not in names:
            session.add(Eventnames(event_name=func))
    session.commit()
    session.close()

create_new_database()
create_eventnames()
print('DONE: init db')

# 'takuto' + 'itoi' == 'takutoitoi'
# print('takuto', 'itoi')
# print(str(i) + ' is not a leap year')
# print('{0} is not a leap year'.format(i))
# print(i, 'is not a leap year')

# for i in range(int(input())):
#     print(i, 'is', end='')
#     if i % 400 != 0 and i % 100 == 0 or i % 4 != 0:
#         print('not')
#     print(' a leap year')