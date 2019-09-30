from flask_login import UserMixin

from app import login, query_db


class User(UserMixin):
    def __init__(self, username, first_name, last_name, password, education="", employment="", music="", movie="",
                 nationality="", birthday="", id=0, active=True):
        self.id = id  # Never persisted
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.active = active
        self.education = education
        self.employment = employment
        self.music = music
        self.movie = movie
        self.nationality = nationality
        self.birthday = birthday

    def get_id(self):
        return self.username

    def persist(self):
        query_db('INSERT INTO Users (username, first_name, last_name, password) VALUES("{}", "{}", "{}", "{}");'.format(
            self.username, self.first_name, self.last_name, self.password))

    def update(self):
        query_db(
            'UPDATE Users SET education="{}", employment="{}", music="{}", movie="{}", nationality="{}", birthday=\'{}\' WHERE username="{}" ;'.format(
                self.education, self.employment, self.music, self.movie, self.nationality,
                self.birthday, self.username
            ))

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.id == other.id

def get_user_by_username(user_name):
    try:
        query = query_db('SELECT * FROM Users WHERE username == "{}";'.format(user_name), one=True)
        user = User(query["username"], query["first_name"], query["last_name"], query["password"], query["education"],
                    query["employment"], query["music"], query["movie"], query["nationality"], query["birthday"],
                    query["id"])
        return user
    except:
        return None


def get_user_by_id(user_id):
    try:
        query = query_db('SELECT * FROM Users WHERE id == "{}";'.format(user_id), one=True)
        user = User(query["username"], query["first_name"], query["last_name"], query["password"], query["education"],
                    query["employment"], query["music"], query["movie"], query["nationality"], query["birthday"],
                    query["id"])
        return user
    except:
        return None


@login.user_loader
def load_user(user_id):
    return get_user_by_username(user_id)
