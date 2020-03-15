from flask import (Flask, jsonify, redirect, session, make_response, 
                   flash, request, render_template)
from functools import wraps
from model import User, Friend, Post, Comment, db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash("You must be logged in to see the page.")
            return redirect('/')
        return func(*args, **kwargs)

    return decorated_function


@app.route('/')
def index():
    """Show the sign up/login page."""

    return render_template('index.html')


@app.route('/feed')
@login_required
def show_feed():
    """Show the logged in user's customized feed."""
    user_id = session.get('user_id')
    user = User.query.get(user_id)

    return render_template('feed.html',user=user)

@app.route('/posts_for_feed')
@login_required
def posts_for_feed():
    """ return the posts for logged in user's feed"""
    user_id = session.get('user_id')
    posts = Friend.query.join(Post, db.and_(Post.user_id == Friend.user_2,
                                Post.active == True)).outerjoin(Comment, db.and_(Comment.post_id == Post.post_id,
                                Comment.active == True)).filter(Friend.user_1 == user_id,
                                Friend.active == True).all()
    post_list = []
    for post in posts:
        post_list.append(post.to_dict_for_json())

    resp = make_response(jsonify(post_list), 200)
    return resp


@app.route('/posts_for_user_feed')
@login_required
def users_posts():
    """ return the users's posts"""

    user_id = session.get('user_id')
    posts = Post.query.outerjoin(Comment, db.and_(Comment.post_id == Post.post_id, 
                                Comment.active == True)).filter(Post.user_id == user_id,
                                Post.active == True).all()
    post_list = []
    for post in posts:
        post_list.append(post.to_dict_for_json())

    resp = make_response(jsonify(post_list), 200)

    return resp


@app.route('/signup', methods=['POST'])
def signup():
    email_address = request.form.get('email_address')
    email_in_use = User.query.filter_by(email_address=email_address).first()

    if email_in_use:
        flash('User not created. Email already in use.')
        return redirect('/')

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    signup_password = request.form.get('signup_password')

    new_user = User(first_name=first_name, 
                    last_name=last_name,
                    email_address=email_address,
                    password=generate_password_hash(signup_password),
                    created_on=datetime.today(),
                    modified_on=datetime.today(),
                    public=True, active=True)

    db.session.add(new_user)
    db.session.commit()

    flash('User created successfully. Please log in.')
    return redirect('/')


@app.route('/login', methods=['POST'])
def login():

    content = request.get_json()
    unhashed_password = content['password']
    email = content['email']

    user = User.query.filter_by(email_address=email).first()

    resp_dict = {}
    if user and check_password_hash(user.password, unhashed_password):
        resp_dict['success'] = True
        session['user_id'] = user.user_id
        flash('You are logged in.')
    else :
        resp_dict['success'] = False

    resp = make_response(jsonify(resp_dict), 200)
    return resp


@app.route('/logout', methods=['POST'])
def logout():
    if session.get('user_id'):
        del session['user_id']

    flash('You have been logged out.')
    resp = make_response(jsonify({'logged_out': True}), 200)
    return resp


@app.route('/user/<int:user_id>')
@login_required
def show_user(user_id):
    """Show the user's posts """
    user = User.query.get(user_id)

    return render_template('user.html',user=user)


@app.route('/add_post', methods=['POST'])
@login_required
def add_post():

    content = request.get_json()
    user_id = content['user_id']
    message = content['message']

    post = Post(user_id=user_id, 
                posted_on=datetime.today(), 
                modified_on=datetime.today(),
                message=message,
                active=True)

    db.session.add(post)
    db.session.commit()
    resp = make_response(jsonify(
                        {'success': True, 
                        'post': post.to_dict_for_json()
                        }), 200)
    return resp


@app.route('/add_comment', methods=['POST'])
@login_required
def add_comment():

    content = request.get_json()
    post_id = content['post_id']
    user_id = content['user_id']
    comment = content['comment']

    comment = Comment(post_id=post_id,
                      user_id=user_id,
                      commented_on=datetime.today(),
                      modified_on=datetime.today(),
                      comment=comment,
                      active=True)

    db.session.add(comment)
    db.session.commit()

    resp = make_response(jsonify(
                        {'success': True, 
                        'comment': comment.to_dict_for_json()
                        }), 200)
    return resp


@app.route('/friend', methods=['POST'])
@login_required
def add_friendship():

    user_1 = session['user_id']
    user_2 = request.form.get('friend_user_id')

    friendship = Friend(user_1=user_1, 
                        user_2=user_2, 
                        active=True, 
                        friended_on=datetime.today(),
                        modified_on=datetime.today())

    db.session.add(friendship)
    db.session.commit()

    return redirect('/feed')


@app.route('/search')
@login_required
def search():

    search_term = request.args.get('term')
    user_id = session['user_id']

    results = User.query.filter((User.user_id != user_id) & 
                                ((User.first_name == search_term) | 
                                (User.last_name == search_term))).all()

    return render_template('search.html',results=results)