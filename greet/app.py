from flask import Flask

app = Flask(__name__)


@app.route("/welcome")
def welcome():
    """ welcome page issues a welcome message """
    return "welcome"


@app.route("/welcome/")
def welcome_no_subfolder():
    """ route for welcome but no destination folder """

    return "OOOOoooohhh . . . . so close!"


@app.route("/welcome/<where>")
def welcome_subfolder(where):
    """ welcome home, or back, or wherever! """

    if ((where.lower() == "home") or (where.lower() == "back")):
        return f"welcome {where}"
    else:
        return "Welcome to where ever you are! "
