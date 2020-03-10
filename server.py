from views import app
from model import connect_to_db

if __name__ == "__main__":
    app.secret_key = "ABC"
    app.debug = True
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app)
    app.run(port=5000,host="0.0.0.0")