import os
from peewee import *
import datetime
from flask_login import UserMixin
from playhouse.db_url import connect


if 'ON_HEROKU' in os.environ:
    DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
    DATABASE = SqliteDatabase('90s.sqlite')

class User(UserMixin, Model):
    username = CharField(unique=True)
    password = CharField()
    class Meta:
        database = DATABASE


class Post(Model):
    title = CharField()
    img = CharField()
    description = CharField()
    likes = IntegerField(default=0)
    owner = ForeignKeyField(User, backref='posts')
    tags = CharField([])
    created_at = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = DATABASE

class Likes (Model):
    user = ForeignKeyField(User, backref="likes")
    post = ForeignKeyField(Post, backref="likes")
    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Post, Likes], safe=True)
    print("tables created")
    DATABASE.close()