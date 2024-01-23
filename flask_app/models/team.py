from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import player, user


class Team:
    db_name = "nba_players_and_teams_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.city = data["city"]
        self.team_name = data["team_name"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.players = [] #empty list to hold MANY players associated with a team
        self.user = None
    @classmethod
    def create_team(cls, data):
        query = """
                INSERT INTO teams(city, team_name, user_id)
                VALUES(%(city)s, %(team_name)s, %(user_id)s);
                """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_all_teams(cls):
        query = """
                SELECT * from teams
                JOIN users
                ON teams.user_id = users.id;
                """ 
        results = connectToMySQL(cls.db_name). query_db(query)# List of dictionaries
        all_teams = [] #will hold team objects
        for team in results: #parse results lists from DB 
            new_team_object = cls(team)
            user_and_team = {
                "id": team["users.id"],
                "first_name": team["first_name"],
                "last_name": team["last_name"],
                "email": team["email"],
                "password": team["password"],
                "created_at": team["users.created_at"],
                "updated_at": team["users.updated_at"],
            }
            user_object= user.User(user_and_team)
            new_team_object.user = user_object
            all_teams.append(new_team_object) #create a team object from each dictionary by calling on cls() and add it to the empty list
        return all_teams
    
    @classmethod
    def get_one_team(cls, data):
        query = """
                SELECT * FROM teams
                WHERE id = %(id)s;
                """
        results = connectToMySQL(cls.db_name).query_db(query, data)#list of dictionary
        if len(results)== 0:
            return None
        else:
            new_team_object = cls(results[0])
            #grab one object
            return new_team_object

    
    @classmethod
    def get_one_team_with_players(cls, data):
        #show the players on each teams roster
        query = """
                SELECT * FROM teams
                LEFT JOIN players
                ON teams.id = players.team_id
                LEFT JOIN users
                ON teams.user_id = users.id
                WHERE teams.id = %(id)s;
                """
        #LEFT JOIN to show teams even if no players are on the roster
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            return None
        team = cls(results[0])
        for each_player in results:
            player_data = {
                "id": each_player["players.id"],
                "first_name": each_player["first_name"],
                "last_name": each_player["last_name"],
                "position": each_player["position"],
                "number": each_player["number"],
                "age": each_player["age"],
                "created_at": each_player["players.created_at"],
                "updated_at": each_player["players.updated_at"]
            }
            new_player = player.Player(player_data)
            team.players.append(new_player) #creating a object with the self.players attribute
            #users information in a dictionary at index [0]
        user_dictionary = {
            "id": results[0]["users.id"],
            "first_name": results[0]["first_name"],
            "last_name": results[0]["last_name"],
            "email": results[0]["email"],
            "password": results[0]["password"],
            "created_at": results[0]["users.created_at"],
            "updated_at": results[0]["users.updated_at"],
        }
        user_object = user.User(user_dictionary)
        team.user = user_object
            #grab one object
        return team
        

    @classmethod
    def update_team(cls, data):
        query = """
                UPDATE teams SET city = %(city)s,
                team_name = %(team_name)s
                WHERE id = %(id)s;
                """
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def delete_team(cls, data):
        query = "DELETE FROM teams WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
#validation for creating a team
    @staticmethod
    def validate_team(form_data):
        is_valid = True
        if len(form_data["city"]) < 2:
            flash("City must be AT LEAST 2 characters", "team_add")
            is_valid = False
        if len(form_data["team_name"]) < 2:
            flash("Team name must be AT LEAST 3 characters", "team_add")
            is_valid = False
        return is_valid
