from views import app
from model import connect_to_db
from flask_debugtoolbar import DebugToolbarExtension

if __name__ == "__main__":
    app.secret_key = "ABC"
    app.debug = True
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app)
    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(port=5000,host="0.0.0.0")