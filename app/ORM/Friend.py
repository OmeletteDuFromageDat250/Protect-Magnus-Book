from app import query_db
from app.ORM.User import get_user_by_id


class Friend:
    def __init__(self, user, friend, id=0):
        self.id = id  # Never persisted
        self.user = user
        self.friend = friend

    def persist(self):
        query_db('INSERT INTO Friends (u_id, f_id) VALUES({}, {});'.format(
            self.user.id,
            self.friend.id))

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.id == other.id


def get_all_friends_by_user(user):
    query = query_db(
        'SELECT * FROM Friends AS f JOIN Users as u ON f.f_id=u.id WHERE f.u_id={} AND f.f_id!={} ;'.format(
            user.id,
            user.id))
    friends = []
    for e in query:
        user = get_user_by_id(e["u_id"])
        friend = get_user_by_id(e["f_id"])
        friends.append(Friend(user, friend, e["id"]))
    return friends
