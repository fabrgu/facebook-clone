from flask import Flask, jsonify, make_response, flash, request
from model import User, Friend, Post, Comment

app = Flask(__name__)

@app.route('/')
def index():
    """Show the sign up/login page."""

    return render_template('index.html')

@app.route('/feed')
def show_feed():
    """Show the logged in user's customized feed."""

    return render_template('feed.html')

@app.route('/user/<int:user_id>')
def show_user(user_id):
    """Show the user's posts """

    return render_template('user.html')

@app.route('/post', methods=['POST'])
def add_post():

    resp = make_response(status=200)
    return resp

@app.route('/comment', methods=['POST'])
def add_comment():

    resp = make_response(status=200)
    return resp

@app.route('/friend', methods=['POST'])
def add_friendship():

    resp = make_response(status=200)
    return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)