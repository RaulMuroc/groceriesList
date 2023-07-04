import sqlite3
import random
from flask import Flask, session, render_template, request, g
import os.path

app = Flask(__name__)
app.secret_key = "b_itu!_'Ggmñp"
app.config["SESSION_COOKIE_NAME"] = "this_is_the_name_of_my_cookie"

@app.route('/', methods=["POST", "GET"])
def index():
    session["the_data"], session["shopping_list"] = get_db()
    return render_template("index.html", the_data=session["the_data"], shopping_list=session["shopping_list"])

@app.route("/add_items", methods=["post"])
def add_items():
    session["shopping_list"].append(request.form["the_data"])
    return request.form["list_of_items"]

@app.route("/remove_items", methods=["post"])
def remove_items():
    return request.form["list_of_items"]

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "grocery_list.db")
        db = g._database = sqlite3.connect(db_path)
        cursor = db.cursor()
        cursor.execute("select name from groceries")
        all_data = cursor.fetchall()
        all_data = [str(val[0]) for val in all_data]
        shopping_list = all_data.copy()
        random.shuffle(shopping_list)
        shopping_list = shopping_list[:5]
    return all_data, shopping_list

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run()