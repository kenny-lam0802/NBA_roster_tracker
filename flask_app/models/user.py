from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re #import regex
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    db_name = "nba_players_and_teams_schema"
    def __init__(self, data):
        self.id = data["id"],
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.team = []
        
    @staticmethod
    def validate_user_registration(user_data):
        is_valid = True
        if len(user_data["first_name"]) < 3:
            is_valid = False
            flash("Please enter a first name of AT LEAST 3 characters" , "registration")
        if len(user_data["last_name"]) < 3:
            is_valid = False
            flash("Please enter a last name of AT LEAST 3 characters", "registration")
        if not EMAIL_REGEX.match(user_data["email"]):
            is_valid = False
            flash("Please enter valid email", "registration")
        if len(user_data["password"]) <8:
            is_valid=False
            flash("Password must contain AT LEAST 8 characters", "registration")
        if user_data["password"] != user_data["confirm_password"]:
            is_valid = False
            flash("Passwords do not match")
        #check DB for email to avoid duplicates
        matching_user = User.get_user_by_email({"email": user_data["email"]})
        if matching_user != None:
            is_valid = False
            flash("Email address unavailable. Please Choose a different email", "registration")
        return is_valid
    
    @classmethod
    def register_user(cls, data):
        query = """
                INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
                """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    #method to determine current logged in user and save in session "by id"
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * from users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data) #creates a list of dictionary
        return cls(results[0]) #create object using dictionary at index 0

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * from users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        #No user found
        if len(results) == 0:
            return None
        return cls(results[0])