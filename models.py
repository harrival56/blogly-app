from enum import unique
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import true

db = SQLAlchemy()
def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'



    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)
    position = db.Column(db.String, nullable=False)
    c_of_origin = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=False)
    post = db.relationship('Post', backref="user")


    def greet(self):
        return f"Hi welcome to my profile page, I'm {self.full_name()}"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


    def __repr__(self):
        u = self
        return f"ID={u.id}, FIRST_NAME={u.first_name}, LAST_NAME={u.last_name}, POSITION={u.position}, C_OF_ORIGIN={u.c_of_origin}"

class Post(db.Model):
    __tablename__ = "posts"


    id  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    tags = db.relationship("PostTag", backref="post_table")
    hashtag = db.relationship("Tag", secondary="post_tags", backref="post_table")

    def __repr__(self):
        return f"ID={self.id}, TITLE={self.title}, CONTENT={self.content}, USER_ID={self.user_id}"


    
class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True)
    pTags = db.relationship("PostTag", backref="tag_table")

    def __repr__(self):
        return f"ID={self.id}, NAME={self.name}"



class PostTag(db.Model):
    __tablename__ = "post_tags"


    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    tag_id = db.Column(db.Text, db.ForeignKey("tags.name"), primary_key=True)

    def __repr__(self):
        return f"POST_ID={self.post_id}, TAG_ID={self.tag_id}"