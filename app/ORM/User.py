from flask_login import UserMixin

from app import login, query_db


class User(UserMixin):
    def __init__(self, username, first_name, last_name, password, id=0, active=True):
        self.id = id  # Never persisted
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.active = active

    def get_id(self):
        return self.username

    def persist(self):
        query_db('INSERT INTO Users (username, first_name, last_name, password) VALUES("{}", "{}", "{}", "{}");'.format(
            self.username, self.first_name, self.last_name, self.password))


def get_user_by_username(user_name):
    return query_db('SELECT * FROM Users WHERE username == "{}";'.format(user_name), one=True)


@login.user_loader
def load_user(user_id):
    query = get_user_by_username(user_id)
    try:
        user = User(query["username"], query["first_name"], query["last_name"], query["password"], query["id"])
        return user
    except:
        return None
