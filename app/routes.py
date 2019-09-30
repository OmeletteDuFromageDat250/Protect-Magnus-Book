from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user

from app import app, query_db
from app.ORM.Post import Post, get_all_posts_by_user
from app.ORM.User import get_user_by_username
from app.forms import IndexForm, PostForm, FriendsForm, ProfileForm, CommentsForm
from datetime import datetime
import os


# this file contains all the different routes, and the logic for communicating with the database

# home page/login/registration
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = IndexForm()
    if form.login.is_submitted() and form.login.submit.data:  # Login
        if form.login.validate_on_submit():
            user = form.login.get_authenticated_user()
            if user:
                login_user(user)
                return redirect(url_for('stream', username=form.login.username.data))
            else:
                flash('Sorry, this user does not exist!')
        else:
            flash('Sorry, wrong password!')
    elif form.register.is_submitted() and form.register.submit.data:  # Register
        if form.register.validate_on_submit():
            form.register.validate_parameters()
            return redirect(url_for('index'))
    return render_template('index.html', title='Welcome', form=form)


@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("index"))


# content stream page
@app.route('/stream/<username>', methods=['GET', 'POST'])
@login_required
def stream(username):
    user = get_user_by_username(username)
    if current_user.id != user.id:
        flash("You don't have access to this section")
        return redirect(url_for("stream", username=current_user.username))

    form = PostForm()
    if form.validate_on_submit():
        if form.image.data:
            path = os.path.join(app.config['UPLOAD_PATH'], form.image.data.filename)
            form.image.data.save(path)

        post = Post(user,
                    form.content.data,
                    form.image.data.filename)
        post.persist()
        return redirect(url_for('stream', username=username))

    posts = get_all_posts_by_user(user)

    return render_template('stream.html', title='Stream', username=username, form=form, posts=posts)


# comment page for a given post and user.
@app.route('/comments/<username>/<int:p_id>', methods=['GET', 'POST'])
@login_required
def comments(username, p_id):
    form = CommentsForm()
    if form.is_submitted():
        user = query_db('SELECT * FROM Users WHERE username="{}";'.format(username), one=True)
        query_db('INSERT INTO Comments (p_id, u_id, comment, creation_time) VALUES({}, {}, "{}", \'{}\');'.format(p_id,
                                                                                                                  user[
                                                                                                                      'id'],
                                                                                                                  form.comment.data,
                                                                                                                  datetime.now()))

    post = query_db('SELECT * FROM Posts WHERE id={};'.format(p_id), one=True)
    all_comments = query_db(
        'SELECT DISTINCT * FROM Comments AS c JOIN Users AS u ON c.u_id=u.id WHERE c.p_id={} ORDER BY c.creation_time DESC;'.format(
            p_id))
    return render_template('comments.html', title='Comments', username=username, form=form, post=post,
                           comments=all_comments)


# page for seeing and adding friends
@app.route('/friends/<username>', methods=['GET', 'POST'])
@login_required
def friends(username):
    form = FriendsForm()
    user = query_db('SELECT * FROM Users WHERE username="{}";'.format(username), one=True)
    if form.is_submitted():
        friend = query_db('SELECT * FROM Users WHERE username="{}";'.format(form.username.data), one=True)
        if friend is None:
            flash('User does not exist')
        else:
            query_db('INSERT INTO Friends (u_id, f_id) VALUES({}, {});'.format(user['id'], friend['id']))

    all_friends = query_db(
        'SELECT * FROM Friends AS f JOIN Users as u ON f.f_id=u.id WHERE f.u_id={} AND f.f_id!={} ;'.format(user['id'],
                                                                                                            user['id']))
    return render_template('friends.html', title='Friends', username=username, friends=all_friends, form=form)


# see and edit detailed profile information of a user
@app.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    user = get_user_by_username(username)
    form = ProfileForm()
    if current_user.id == user.id:
        if form.is_submitted() and form.validate():
            user.education = form.education.data
            user.employment = form.employment.data
            user.music = form.music.data
            user.movie = form.movie.data
            user.nationality = form.nationality.data
            user.birthday = form.birthday.data
            user.update()
            return redirect(url_for('profile', username=username))
        else:
            return render_template('profile.html', title='profile', username=username, user=user, form=form)
    else:
        return render_template('profile.html', title='profile', username=username, user=user)
