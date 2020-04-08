from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from server import app, db, configure_db, connect_to_db

class ModelMixin:

    def save(self):
        db.session.add(self)
        db.session.commit()


    def update(self):
        db.session.commit()


class User(ModelMixin, db.Model): 
    """ Data model for a user. """
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email_address = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    modified_on = db.Column(db.DateTime, nullable=False)
    public = db.Column(db.Boolean, nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        """Return a human-readable representation of a User."""

        return (f'<User user_id={self.user_id}'
            f' first_name={self.first_name} last_name={self.last_name}'
            f' email_address={self.email_address}')

    def to_dict_for_json(self):
        json_dict = {}
        json_dict['user_id'] = self.user_id
        json_dict['first_name'] = self.first_name
        json_dict['last_name'] = self.last_name

        return json_dict


class Friend(ModelMixin, db.Model):
    """ Data model for a friendship. """
    __tablename__ = "friends"

    friend_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_1 = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    user_2 = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    friended_on = db.Column(db.DateTime, nullable=False)
    modified_on = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        """Return a human-readable representation of a friendship."""

        return (f'<Friend user_1={self.user_1}'
            f' user_2={self.user_2}')


class Post(ModelMixin, db.Model):
    """ Data model for a post. """
    __tablename__ = "posts"

    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    posted_on = db.Column(db.DateTime, nullable=False)
    modified_on = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.String(500), nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    # Define relationship to User
    user = db.relationship("User", backref="posts", order_by=post_id)
    # Define relationship to Comment
    comments = db.relationship("Comment")

    def __repr__(self):
        """Return a human-readable representation of a Post."""
        return f'<Post post_id={self.post_id} user_id={self.user_id}'

    def to_dict_for_json(self):
        json_dict = {}
        json_dict['post_id'] = self.post_id
        json_dict['user_id'] = self.user_id
        json_dict['posted_on'] = self.posted_on.strftime('%b %d, %Y %H:%M:%S')
        json_dict['modified_on'] = self.modified_on.strftime('%b %d, %Y %H:%M:%S')
        json_dict['message'] = self.message
        json_dict['user'] = self.user.to_dict_for_json()
        json_dict['comments'] = []
        for comment in self.comments:
            json_dict['comments'].append(comment.to_dict_for_json())

        return json_dict


class Comment(ModelMixin, db.Model):
    """ Data model for a comment. """
    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    commented_on = db.Column(db.DateTime, nullable=False)
    modified_on = db.Column(db.DateTime, nullable=False)
    comment = db.Column(db.String(500), nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    # Define relationship to Post
    post = db.relationship("Post", order_by=comment_id)

    #Define relationship to User
    user = db.relationship("User", backref="comments")

    def __repr__(self):
        """Return a human-readable representation of a Comment."""
        return (f'<Comment comment_id={self.comment_id}'
                f' post_id={self.post_id} user_id={self.user_id}')

    def to_dict_for_json(self):
        json_dict = {}
        json_dict['comment_id'] = self.comment_id
        json_dict['post_id'] = self.post_id
        json_dict['user_id'] = self.user_id
        json_dict['commented_on'] = self.commented_on.strftime('%b %d, %Y %H:%M:%S')
        json_dict['modified_on'] = self.modified_on.strftime('%b %d, %Y %H:%M:%S')
        json_dict['comment'] = self.comment
        json_dict['user'] = self.user.to_dict_for_json()

        return json_dict


if __name__ == "__main__":
    # As a convenience, if this module is run interactively, it will leave
    # you in a state of being able to work with the database directly.
    from flask import Flask
    current_app = Flask(__name__)
    configure_db(current_app)
    connect_to_db(current_app)
    db.create_all()
    print("Connected to db.")