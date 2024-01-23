from flask_app import app #importing app from __init.py
from flask_app.controllers import teams, players, users #import controllers for routing


if __name__== "__main__":
    app.run(debug=True)