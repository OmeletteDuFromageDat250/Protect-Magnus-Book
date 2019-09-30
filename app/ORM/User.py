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
        self.friends = []

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

    def persist_friends(self):
        for e in self.friends:
            if e.id is None:
                query_db('INSERT INTO Friends (u_id, f_id) VALUES({}, {});'.format(
                    e.user.id,
                    e.friend.id))
            else:
                query_db('UPDATE Friends SET u_id="{}", f_id="{}" WHERE u_id="{}";'.format(
                    e.user.id,
                    e.friend.id,
                    e.user.id))

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.id == other.id


def get_user_by_username(user_name):
    try:
        query = query_db('SELECT * FROM Users WHERE username == "{}";'.format(user_name), one=True)
        user = User(query["username"], query["first_name"], query["last_name"], query["password"], query["education"],
                    query["employment"], query["music"], query["movie"], query["nationality"], query["birthday"],
                    query["id"])
        user.friends = get_all_friends_by_user(user.id)
        return user
    except Exception as e:
        return None


def get_user_by_id(user_id):
    try:
        query = query_db('SELECT * FROM Users WHERE id == "{}";'.format(user_id), one=True)
        user = User(query["username"], query["first_name"], query["last_name"], query["password"], query["education"],
                    query["employment"], query["music"], query["movie"], query["nationality"], query["birthday"],
                    query["id"])
        user.friends = get_all_friends_by_user(user)
        return user
    except:
        return None


def get_all_friends_by_user(user_id):
    query = query_db(
        'SELECT * FROM Friends AS f JOIN Users as u ON f.f_id=u.id WHERE f.u_id="{}" AND f.f_id!="{}" ;'.format(
            user_id,
            user_id))
    friends = []
    for e in query:
        friend = get_user_by_id(e["f_id"])
        friends.append(friend)
    return friends


@login.user_loader
def load_user(user_id):
    return get_user_by_username(user_id)
