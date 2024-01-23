from flask_app.config.mysqlconnection import connectToMySQL #import function to connect to DB
from flask_app.models import team, user
from flask import flash

class Player:
    db_name = "nba_players_and_teams_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.position = data["position"]
        self.number = data["number"]
        self.age = data["age"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.team = None #connects ONE team to this player
        self.user = None

    @classmethod
    def add_player(cls, data):
        query = """
                INSERT INTO players 
                (first_name, last_name, position, number, age, team_id, user_id)
                VALUES (%(first_name)s, %(last_name)s, %(position)s, %(number)s, %(age)s, %(team_id)s, %(user_id)s);
                """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_all_players_and_teams(cls):
        query = """
                SELECT * from players
                JOIN teams
                ON players.team_id = teams.id
                JOIN users
                ON players.user_id = users.id;
                """
        results = connectToMySQL(cls.db_name).query_db(query)
        all_players_objects = [] #store all players
        for each_player in results:
        #Create a Player
            new_player = cls(each_player)
        #Create the self.team object
            new_team = {
                "id": each_player["teams.id"],#duplictate atrribute from both tables
                "city": each_player["city"],
                "team_name": each_player["team_name"],
                "created_at": each_player["teams.created_at"], #duplictate atrribute from both tables
                "updated_at": each_player["teams.updated_at"], #duplictate atrribute from both tables
            }

            new_team_object = team.Team(new_team)
            new_player.team = new_team_object
            new_user_dictionary = {
                "id": each_player["users.id"],
                "first_name": each_player["users.first_name"],
                "last_name": each_player["users.last_name"],
                "email": each_player["email"],
                "password": each_player["password"],
                "created_at": each_player["users.created_at"],
                "updated_at": each_player["users.updated_at"],
            }
            new_user_object = user.User(new_user_dictionary)
            new_player.user = new_user_object
            all_players_objects.append(new_player)
        return all_players_objects
    
    @classmethod
    def get_one_player_with_team(cls, data):
        #can do JOIN because every player must be linked to a team through team_id
        query = """
                SELECT * FROM players
                JOIN teams ON  players.team_id = teams.id
                WHERE players.id = %(id)s;
                """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        this_player = cls(results[0]) #create a player object at index [0]
        #new ONE object due to duplicate columns from each table
        new_team_dictionary = {
            "id": results[0]["teams.id"],#duplicate column
            "city": results[0]["city"],
            "team_name": results[0]["team_name"],
            "created_at": results[0]["teams.created_at"], #duplicate column
            "updated_at": results[0]["teams.updated_at"], #duplicate column
        }

        new_team = team.Team(new_team_dictionary)
        #link team to player
        this_player.team = new_team
        return this_player
    
    @classmethod
    def update_player(cls, data):
        query = """
                UPDATE players SET
                first_name = %(first_name)s,
                last_name = %(last_name)s,
                position = %(position)s,
                number = %(number)s,
                age = %(age)s,
                team_id = %(team_id)s
                WHERE 
                id = %(id)s;
                """
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def delete_player(cls, data):
        query = "DELETE FROM players WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @staticmethod
    def validate_player(player):
        is_valid = True
        if len(player["first_name"]) < 2:
            flash("Please enter a First Name", "player")
            is_valid = False
        if len(player["last_name"]) < 2:
            flash("Please enter a Last Name", "player")
            is_valid = False
        if len(player["position"]) < 0:
            flash("Please enter a player position(s)", "player")
            is_valid = False
        if player["number"] == '' or int(player['number']) < 0:
            flash("Please enter the player's number", "player")
            is_valid = False
        if player["age"] == '' or int(player['age']) < 15:
            flash("Invalid age", "player")
            is_valid = False
        return is_valid