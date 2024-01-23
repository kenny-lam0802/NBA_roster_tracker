from flask import render_template, redirect, request, session,flash
from flask_app.models import user
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def login_page():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard_page():
    #only user is session can access this page
    if "user_id" not in session:
        flash("Please Log In")
        return redirect("/")
        
    data={
        "id": session["user_id"]
    }
    logged_in_user = user.User.get_user_by_id(data)

    return render_template("dashboard.html" , logged_in_user = logged_in_user)

@app.route("/register", methods = ["POST"])
def register_user():
    if not user.User.validate_user_registration(request.form):
        return redirect("/")
    else:
        pw_hash = bcrypt.generate_password_hash(request.form["password"])
        #Created a new data dictionary and call on the hashed password to be added to the DB
        data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "password": pw_hash
        }
        session["user_id"] = user.User.register_user(data)
        return redirect("/teams")

@app.route("/login", methods = ["POST"])
def login_user():
    #search DB to ensure email exists
    data = {
        "email":request.form["email"]
    }
    user_in_db = user.User.get_user_by_email(data)
    if not user_in_db:
        flash("Please enter a valid Email/Password or Register", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Please enter a valid Email/Password or Register", "login")
        return redirect('/')
    #if all credentials met, set user into session
    session['user_id'] = user_in_db.id
    return redirect("/teams")
    
    
@app.route("/logout")
def logout_user():
    session.clear()
    return redirect('/')