import datetime

from app import query_db
from app.ORM.User import get_user_by_id


class Post():
    def __init__(self, user, content, image, creation_time=datetime.datetime.now(), id=0):
        self.id = id  # Never persisted
        self.user = user
        self.content = content
        self.image = image
        self.creation_time = creation_time

    def persist(self):
        query_db('INSERT INTO Posts (u_id, content, image, creation_time) VALUES({}, "{}", "{}", \'{}\');'.format(
            self.user.id,
            self.content,
            self.image,
            self.creation_time))


def get_all_posts_by_user(user):
    query = query_db(
        'SELECT p.*, u.*, (SELECT COUNT(*) FROM Comments WHERE p_id=p.id) AS cc FROM Posts AS p JOIN Users AS u ON u.id=p.u_id WHERE p.u_id IN (SELECT u_id FROM Friends WHERE f_id={0}) OR p.u_id IN (SELECT f_id FROM Friends WHERE u_id={0}) OR p.u_id={0} ORDER BY p.creation_time DESC;'.format(
            user.id))
    posts = []
    for e in query:
        user = get_user_by_id(e["u_id"])
        posts.append(Post(user, e["content"], e["image"], e["creation_time"], e["id"]))
    return posts
