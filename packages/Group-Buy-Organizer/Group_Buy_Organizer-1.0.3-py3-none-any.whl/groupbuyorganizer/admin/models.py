from flask_login import UserMixin

from datetime import datetime

from groupbuyorganizer import database, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(database.Model, UserMixin):

    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(20), unique=True, nullable=False)
    password = database.Column(database.String(60), nullable=False)
    email = database.Column(database.String(120), unique=True, nullable=False)
    disabled = database.Column(database.Boolean, nullable=False, default=False)
    is_admin = database.Column(database.Boolean, nullable=False, default=False)
    is_root = database.Column(database.Boolean, nullable=False, default=False)
    date_created = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Instance(database.Model):

    id = database.Column(database.Integer, primary_key=True)
    root_created = database.Column(database.Boolean, nullable=False, default=False)
    registration_enabled = database.Column(database.Boolean, nullable=False, default=True)
    users_can_see_master_overview = database.Column(database.Boolean, nullable=False, default=True)
    wkhtmltopdf_path = database.Column(database.String(256), nullable=True)


class Category(database.Model):

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(100), nullable=False, unique=True)
    items = database.relationship('Item', backref='category', lazy=True)