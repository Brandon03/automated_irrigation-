import os
import sqlite3
from flask import Flask
from flask import request
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from flask import abort
from flask import render_template
from flask import flash

import pdb

app = Flask(__name__) # create application instance.
app.config.from_object(__name__) # load config from this file, flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, "flaskr.db"),
    SECRET_KEY="development key", # what is secret key? keep client-side sessions secure
    USERNAME="admin",
    PASSWORD="default"
))
app.config.from_envvar("FLASKR_SETTINGS", silent=True)
#1. environment var FLASKR_SETTING points to a config file to be loaded
#2. can use the from_object() method on the config object and provide it \
# with an import name of a module.
#3. Flask will then initialize the variable from that module. Note that in
#all cases, only variable names that are uppercase are considered.
def connect_db():
    """ Connects to the specific database."""
    rv = sqlite3.connect(app.config["DATABASE"])
    rv.row_factory = sqlite3.Row
    return rv

## CREATING DATABASE ------------------
def init_db():
    db = get_db()
    # open_resource is helper function that open resource that application support
    with app.open_resource("schema.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command("initdb") # decorator register new command with flask script.
def initdb_command():
    """initializes the database"""
    init_db()
    print("Initialized the database.")
## -----------------------------------

# Utilizing application context ensure one request at a time uses connection.
# Flask provides 2 context: The application context and request context

# request, request object associated with current request.
# g, general purpose variable associated with current application context.
# information can be store at g object safety.

def get_db():
    """
    Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = connect_db()
    return g.sqlite_db

# app.teardown_appcontext will be called when app context tear down
# app context is created before the request comes in and destroyed(tear down)
# when reuest completed.

# Reasons of teardown:
# 1. everything went well (error parameter is None)
# 2. exception happened. (error is passed to tear down function)

@app.teardown_appcontext
def close_db(error):
    """ closes the database again at the end of the request"""
    if hasattr(g, "sqlite.db"):
        g.sqlite_db.close()

## THE VIEW FUNCTIONS ----------------------

# Show entries
@app.route("/")
def show_entries():
    """ show all entries stored in database """
    db = get_db()
    cur = db.execute("Select * from entries")
    entries = cur.fetchall()
    return render_template("show_entries.html", entries=entries)

# Add new entry (if user is logged in)
# it only responds to POST request
@app.route("/add", methods=["POST"])
def add_entry():
    if not session.get("logged_in"):
        abort(401) # 401 is unauthorized error
    db = get_db()
    db.execute("insert into entries (title, text) values (?, ?)",
               [request.form["title"], request.form["text"]])
    # make sure ? is used for sqlite to prevent SQL injection
    db.commit()
    flash("New entry was successfully posted")
    return redirect(url_for("show_entries"))

# Login and Logout
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] != app.config["USERNAME"]:
            error = "Invalid username"
        elif request.form["password"] != app.config["PASSWORD"]:
            error = "Invalid password"
        else:
            session["logged_in"] = True
            flash("You were logged in")
            return redirect(url_for("show_entries"))
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("You were logged out")
    return redirect(url_for("show_entries"))


