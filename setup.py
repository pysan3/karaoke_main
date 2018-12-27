# pylint: skip-file

# create new database
from database import *
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
session = Session()
session.add(Users(
    id=0,
    user_name='master',
    user_password='hogehoge',
    created_at=0,
))
session.commit()
session.close()

