from flask import render_template, request, redirect, session,flash
from flask_app import app
from flask_app.models import player, team, user

@app.route("/players")
def view_players():
    if "user_id" not in session:
        flash("Please Log In")
        return redirect("/")
    all_players = player.Player.get_all_players_and_teams()
    return render_template("all_players.html", all_players = all_players)
    
@app.route("/players/add")
def new_hooper():
    if "user_id" not in session:
        flash("Please Log In")
        return redirect("/")
    else:
        all_teams = team.Team.get_all_teams()
        logged_in_user = user.User.get_user_by_id({"id": session["user_id"]})
        return render_template("add_player.html",  all_teams = all_teams, logged_in_user = logged_in_user)

@app.route("/new/player", methods=["POST"])
def create_new_player():
    if "user_id" not in session:
        return redirect("/")
    if not player.Player.validate_player(request.form):
        return redirect("/players/add")
    form_data={
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "position": request.form["position"],
        "number": request.form["number"],
        "age": request.form["age"],
        "team_id": request.form["team_id"],
        "user_id": session["user_id"],
    }
    player.Player.add_player(form_data)
    return redirect("/players")

@app.route("/players/view/<int:id>")
def one_player(id):
    if "user_id" not in session:
        flash("Please Log In")
        return redirect("/")
    else:
        data ={
            "id":id
        }
        player_info = player.Player.get_one_player_with_team(data)
        return render_template('view_player.html', player_info = player_info)

@app.route("/players/<int:id>/edit")
def edit_player(id):
    if "user_id" not in session:
        flash("Please Log In")
        return redirect("/")
    else:
        data={"id": id}
        one_player = player.Player.get_one_player_with_team(data)#get one player
        all_teams = team.Team.get_all_teams() #get all teams for drop down option
        return render_template("edit_player.html", one_player = one_player, all_teams = all_teams)

@app.route("/players/edit", methods = ["POST"]) #hidden input instead of path variable
def handle_player_edit():
    if "user_id" not in session:
        flash("Please Log In")
        return redirect("/")
    if not player.Player.validate_player(request.form):
        return redirect(f"/players/{request.form['id']}/edit")
    else:
        player.Player.update_player(request.form)
        return redirect("/players")

@app.route("/players/<int:id>/delete")
def delete_player_by_id(id):
    if "user_id" not in session:
        flash("Please Log In")
        return redirect("/")
    else:
        data = {"id": id}
        player.Player.delete_player(data)
        return redirect("/players")