from views import app
from model import connect_to_db

if __name__ == "__main__":
    # from flask_debugtoolbar import DebugToolbarExtension
    app.secret_key = "ABC"
    app.debug = True
    app.jinja_env.auto_reload = app.debug
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    connect_to_db(app)
    # Use the DebugToolbar
    # DebugToolbarExtension(app)
    app.run(port=5000,host="0.0.0.0")