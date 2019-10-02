import datetime

from app import query_db
from app.ORM.User import get_user_by_id


class Comment:
    def __init__(self, post, user, comment, creation_time=datetime.datetime.now(), id=0):
        self.id = id  # Never persisted
        self.post = post
        self.user = user
        self.comment = comment
        self.creation_time = creation_time

    def persist(self):
        query_db('INSERT INTO Comments (p_id, u_id, comment, creation_time) VALUES({}, {}, "{}", \'{}\');'.format(
            self.post.id,
            self.user.id,
            self.comment,
            self.creation_time))

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.id == other.id


def get_all_comments_by_post(post):
    query = query_db(
        'SELECT DISTINCT * FROM Comments AS c JOIN Users AS u ON c.u_id=u.id WHERE c.p_id={} ORDER BY c.creation_time DESC;'.format(
            post.id))
    comments = []
    for e in query:
        user = get_user_by_id(e["u_id"])
        comments.append(Comment(post, user, e["comment"], e["creation_time"], e["id"]))
    return comments
