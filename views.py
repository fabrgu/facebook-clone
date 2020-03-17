from flask import (Flask, jsonify, redirect, session, make_response, 
                   flash, request, render_template)
from functools import wraps
from model import User, Friend, Post, Comment, db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from graph import SocialGraph

app = Flask(__name__)

success_flash = 'success'
err_flash = 'error'

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash('You must be logged in to see the page.', err_flash)
            return redirect('/')
        return func(*args, **kwargs)

    return decorated_function

def get_suggested_friends(user_id):

    friends = Friend.query.filter(Friend.user_1 == user_id, 
                                  Friend.active == True).all()

    # only suggesting friends of friends
    # only user's friends are the keys in the social graph's underlying dict

    social_graph = SocialGraph()
    social_graph.add_friend_node(user_id)
    for friend in friends:
        social_graph.add_friend_edge(user_id, friend.user_2)
        if friend not in social_graph:
            social_graph.add_friend_node(friend.user_2)
            friends_friends = Friend.query.filter(Friend.user_1 == friend.user_2,
                                                  Friend.active == True).all()

            for friend_of_friend in friends_friends:
                social_graph.add_friend_edge(friend.user_2, friend_of_friend.user_2)


    suggested_friends = []
    friend_list = social_graph.get_friend_connections(user_id)

    for friend_user_id in friend_list:
        friends_friend_list = social_graph.get_friend_connections(friend_user_id)
        for friend_of_friend in friends_friend_list:
            if (friend_of_friend != user_id
                and friend_of_friend not in social_graph
                and friend_of_friend not in suggested_friends):
                    user = User.query.get(friend_of_friend)
                    suggested_friends.append(user)
                    if len(suggested_friends) > 1:
                        break

    return suggested_friends


@app.route('/')
def index():
    """Show the sign up/login page."""
    if session.get('user_id'):
        return redirect('/feed')
        
    return render_template('index.html')


@app.route('/feed')
@login_required
def show_feed():
    """Show the logged in user's customized feed."""
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    suggested_friends = get_suggested_friends(user_id)

    return render_template('feed.html', user=user, 
                          suggested_friends=suggested_friends)


@app.route('/posts_for_feed')
@login_required
def posts_for_feed():
    """ return the posts for logged in user's feed"""
    user_id = session.get('user_id')
    friend_posts = Post.query.join(Friend, db.and_(Post.user_id == Friend.user_2,
                                Friend.active == True)).outerjoin(Comment, db.and_(Comment.post_id == Post.post_id,
                                Comment.active == True)).filter(Friend.user_1 == user_id,
                                Post.active == True).order_by(Post.post_id.desc()).all()

    post_list = []
    for post in friend_posts:
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
                                Post.active == True).order_by(Post.post_id.desc()).all()
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
        flash('User not created. Email already in use.', err_flash)
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

    flash('User created successfully. Please log in.', success_flash)
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
        flash('You are logged in.', success_flash)
    else :
        resp_dict['success'] = False

    resp = make_response(jsonify(resp_dict), 200)
    return resp


@app.route('/logout', methods=['POST'])
def logout():
    if session.get('user_id'):
        del session['user_id']

    flash('You have been logged out.', success_flash)
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

    flash('Friend added successfully.', success_flash)

    return redirect('/feed')


@app.route('/search')
@login_required
def search():

    search_term = request.args.get('term')
    user_id = session['user_id']

    results = db.session.query(User, 
                               Friend).outerjoin(Friend, db.and_(Friend.user_1 == user_id, 
                               Friend.active == True)).filter((User.user_id != user_id) & 
                               (User.public == True) & 
                               ((Friend.user_2 == None) |
                                (Friend.user_2 != User.user_id)) &
                               (((User.first_name.like(f'%{search_term}%')) | 
                               (User.last_name.like(f'%{search_term}%'))))).all()

    return render_template('search.html',results=results)


@app.route('/public', methods=['POST'])
@login_required
def change_public():

    public_form = request.form.get('public')
    public = True if public_form == "true" else False
    user_id = request.form.get('user_id', session['user_id'])
    user = User.query.get(user_id)
    user.public = public

    db.session.commit()

    flash('Public option changed successfully.', success_flash)

    return redirect(f'/user/{user_id}')