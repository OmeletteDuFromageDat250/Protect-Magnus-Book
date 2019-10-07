from _sha256 import sha256

from flask_login import login_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FormField, TextAreaField, FileField
from wtforms.fields.html5 import DateField

# defines all forms in the application, these will be instantiated by the template,
# and the routes.py will read the values of the fields
# TODO: Add validation, maybe use wtforms.validators??
# TODO: There was some important security feature that wtforms provides, but I don't remember what; implement it
from wtforms.validators import InputRequired, EqualTo

from app import get_db
from app.ORM.User import load_user, User, get_user_by_username


class LoginForm(FlaskForm):
    username = StringField('Username', render_kw={'placeholder': 'Username'})
    password = PasswordField('Password', render_kw={'placeholder': 'Password'})
    remember_me = BooleanField(
        'Remember me')  # TODO: It would be nice to have this feature implemented, probably by using cookies
    submit = SubmitField('Sign In')

    def get_authenticated_user(self):
        user = load_user(self.username.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.password else None


class RegisterForm(FlaskForm):
    first_name = StringField('First Name', [InputRequired("Invalid first name")], render_kw={'placeholder': 'First Name'})
    last_name = StringField('Last Name', [InputRequired("Invalid last name")], render_kw={'placeholder': 'Last Name'})
    username = StringField('Username', [InputRequired("Invalid username")], render_kw={'placeholder': 'Username'})
    password = PasswordField('Password', [EqualTo('confirm_password', message='Passwords must match')], render_kw={'placeholder': 'Password'})
    confirm_password = PasswordField('Confirm Password', render_kw={'placeholder': 'Confirm Password'})
    submit = SubmitField('Sign Up')

    def validate_parameters(self):
        if load_user(self.username.data) is None:
            m = sha256()
            m.update(self.password.data.encode())
            u = User(username=self.username.data, first_name=self.first_name.data, last_name=self.last_name.data, password=m.hexdigest())
            u.persist()
            return True
        else:
            self.errors["username"] = "Username already in use"
        return False


class IndexForm(FlaskForm):
    login = FormField(LoginForm)
    register = FormField(RegisterForm)


class PostForm(FlaskForm):
    content = TextAreaField('New Post', [InputRequired("This field is required")], render_kw={'placeholder': 'What are you thinking about?'})
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')


class CommentsForm(FlaskForm):
    comment = TextAreaField('New Comment', [InputRequired("This field is required")], render_kw={'placeholder': 'What do you have to say?'})
    submit = SubmitField('Comment')


class FriendsForm(FlaskForm):
    username = StringField('Friend\'s username', render_kw={'placeholder': 'Username'})
    submit = SubmitField('Add Friend')


class ProfileForm(FlaskForm):
    education = StringField('Education', render_kw={'placeholder': 'Highest education'})
    employment = StringField('Employment', render_kw={'placeholder': 'Current employment'})
    music = StringField('Favorite song', render_kw={'placeholder': 'Favorite song'})
    movie = StringField('Favorite movie', render_kw={'placeholder': 'Favorite movie'})
    nationality = StringField('Nationality', render_kw={'placeholder': 'Your nationality'})
    birthday = DateField('Birthday')
    submit = SubmitField('Update Profile')
