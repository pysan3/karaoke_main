import server

def login(data):
    name = data['user_name']
    password = data['user_password']
    return server.login(name, password)

def check_database():
    server.add_users()
    user_dataset = server.return_users()
    for user in user_dataset:
        print(user.id, user.user_name, user.user_password, user.created_at)

def debug():
    check_database()

if __name__ == '__main__':
    debug()