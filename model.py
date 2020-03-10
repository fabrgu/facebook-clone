from flask_sqlalchemy import SQLAlchemy

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
            f' user_2={self.user_2} last_name={self.last_name}')


class Post(db.Model):
    """ Data model for a post. """
    __tablename__ = "posts"

    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    posted_on = db.Column(db.DateTime, nullable=False)
    modified_on = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.String(500), nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        """Return a human-readable representation of a Post."""
        return f'<Post post_id={self.post_id} user_id={self.user_id}'

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

    def __repr__(self):
        """Return a human-readable representation of a Comment."""
        return (f'<Comment comment_id={self.comment_id}'
                f' post_id={self.post_id} user_id={self.user_id}')

# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///facebook-clone'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if this module is run interactively, it will leave
    # you in a state of being able to work with the database directly.
    from server import app
    connect_to_db(app)
    print("Connected to db.")