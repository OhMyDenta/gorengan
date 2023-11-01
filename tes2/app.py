import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Data students
db = SQL("sqlite:///score.db")
app.config.update(SECRET_KEY=os.urandom(24))
@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        
        name = request.form.get("name")
        score = request.form.get("score")
        print(name)
        print(score)
        db.execute("INSERT INTO score (name, score) VALUES(?, ?)", name , score)
        return redirect("/")
    else: 
        students = db.execute("SELECT * FROM score")
        return render_template("index.html", students=students)
    
@app.route("/edit/<id>", methods=["GET","POST"])
def edit_data(id):
    if request.method=="GET":
        score = db.execute("SELECT * FROM score WHERE id = ?" , id)[0]
        print(score)
        return render_template("edit.html", score=score)
    
    elif request.method=="POST":
        score_name = request.form.get("name")
        score_scor = request.form.get("score")
        db.execute('UPDATE score set name = ?, score = ? where id = ?', score_name, score_scor, id)
        return redirect("/")

@app.route("/delete/<id>", methods=["GET","POST"])
def delete_data(id):
    db.execute("delete from score where id = ?", id)
    return redirect("/")

@app.route("/regis", methods=["GET","POST"])
def regis_data():
    
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            return ("must provide Name")
        elif not request.form.get("password"):
            return ("must provide Password")
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        Email = request.form.get("email")
        username = request.form.get("username")
        name = request.form.get("Name")
        Password = request.form.get("password")
        regpassword = request.form.get("regristrasi_password")

        hash = generate_password_hash(Password)
        if len(rows) == 1:
            return ("Name already taken")
        if Password == regpassword:
            db.execute("INSERT INTO users(Email, name, username, password) VALUES(?, ?, ?, ?)",Email, name, username, hash)
            registered_user = db.execute("SELECT * FROM users where username = ?", username)
            session["user_id"] = registered_user[0]["id"]
            flash("You are successfully registered")
            return redirect("/")
        else:
            return render_template("index.html")   
    else:
        return render_template("regis.html")
        
@app.route("/login", methods=["GET","POST"])
def login():
    """log user in"""
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return ("must provide username")
        elif not request.form.get("password"):
            return ("must provide password")
        
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) != 1 or not check_password_hash(rows[0]['password'], request.form.get("password")):
            return("invalid username or password")
        session["users_id"] = rows[0]["id"]
        return redirect("/")
        
    else:
        return render_template("login.html")
    
@app.route("/logout")
def logout():
    """Log user out"""

    session.clear()
    return redirect("/")