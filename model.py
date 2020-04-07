import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Instantiate a SQLAlchemy object. We need this to create our db.Model classes.
db = SQLAlchemy()

class User(db.Model): 
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


class Friend(db.Model):
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


class Post(db.Model):
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


class Comment(db.Model):
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

# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = get_connection_string()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # uncomment to see sql for debugging 
    # app.config['SQLALCHEMY_ECHO'] = True

    db.app = app
    db.init_app(app)

def get_connection_string():
    if 'DATABASE_URL' in os.environ:
        return os.environment['DATABASE_URL']
    else:
        return 'postgresql:///facebook-clone'


if __name__ == "__main__":
    # As a convenience, if this module is run interactively, it will leave
    # you in a state of being able to work with the database directly.
    from server import app
    connect_to_db(app)
    print("Connected to db.")