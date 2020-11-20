from peewee import *
import datetime
from flask_login import UserMixin

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
    tags = CharField([]) ## come back to this you idiot
    created_at = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Post], safe=True)
    print("tables created")
    DATABASE.close()