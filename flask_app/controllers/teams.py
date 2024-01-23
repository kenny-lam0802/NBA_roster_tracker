from flask import render_template, request, redirect, session,flash
from flask_app import app
from flask_app.models import team, user

@app.route("/teams")
def view_all_teams():
    if "user_id" not in session:
        flash("Please Log In")
        return redirect("/")
    else:
        all_teams = team.Team.get_all_teams()
        logged_in_user = user.User.get_user_by_id({"id": session["user_id"]})
        return render_template("all_teams.html", all_teams = all_teams, logged_in_user = logged_in_user)

@app.route("/teams/view/<int:id>")
def view_one_team(id):
    if "user_id" not in session:
        flash("Please Log In")
        return redirect("/")
    else:
        data ={
            "id" :id
        }
        one_team = team.Team.get_one_team_with_players(data)
        return render_template("view_team.html", one_team = one_team)

@app.route("/teams/new")
def add_team_form():
    if "user_id" not in session:
        flash("Please Log In")
        return redirect("/")
    else:
        return render_template("add_team.html")

@app.route("/teams/add", methods = ["POST"])
def handle_team_form():
    if "user_id" not in session:
        redirect("/")
    if not team.Team.validate_team(request.form):
        return redirect('/teams/new')
    form_data={
        "city": request.form["city"],
        "team_name": request.form["team_name"],
        "user_id": session["user_id"], #can also use hidden input
    }
    team.Team.create_team(form_data)
    return redirect("/teams")

@app.route("/teams/edit/<int:id>")
def edit_team(id):
    if "user_id" not in session:
        flash("Please Log In")
        return redirect("/")
    else:
        data = {"id": id}
        this_team = team.Team.get_one_team(data)
        return render_template("edit_team.html", this_team = this_team)

@app.route("/update/team/<int:id>", methods = ["POST"])
def edit_team_form(id):
    if not team.Team.validate_team(request.form):
        return redirect(f"/teams/edit/{id}")
    form_results = {
        "city": request.form["city"],
        "team_name": request.form["team_name"],
        "id": id
    }
    team.Team.update_team(form_results)
    return redirect(f"/teams/view/{id}")# f string to pass in "id"

@app.route("/teams/delete/<int:id>")
def delete_team_by_id(id):
    if "user_id" not in session:
        flash("Please Log In")
        return redirect("/")
    else:
        data = {
            "id":id
        }
        team.Team.delete_team(data)
        return redirect("/teams")