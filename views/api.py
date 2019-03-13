from flask import (Flask, 
                    render_template, 
                    jsonify, flash, 
                    redirect, url_for, request, 
                    Response,session,abort,
                    send_from_directory)
import json 
from werkzeug import secure_filename
from flask import Flask
from models import db, bcrypt
import config
from os import environ 
from flask_bootstrap import Bootstrap

def init_app():
    app = Flask(__name__) 
    app.config.from_object(environ['APP_SETTINGS'])
    Bootstrap(app)
    bcrypt.init_app(app)
    db.init_app(app) 
    return app
db = db    
app = init_app()

@app.route("/")
def home():

    return render_template("home.html")
