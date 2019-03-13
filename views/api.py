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


@app.errorhandler(401)
def error_401(error):
    error = {
        'title':"Error 401 Occured",
        'desc':"You are unathorized to access this resource",
        'tip':"Please first login to access this page.",
        'url':"/",
        'action':"Back to Home Page"
    }
    return render_template("error.html",**locals())

@app.errorhandler(403)
def error_403(error):
    error = {
        'title':"Error 403 Occured",
        'desc':"You are forbidden from accessing this resource",
        'tip':"Contact Admin for details on why.",
        'url':"/contact",
        'action':'Contact Support Team'
    }
    return render_template("error.html",**locals())

@app.errorhandler(404)
def error_404(error):    
    error = {
        'title':"Error 404 Occured!",
        'desc':"Requested Resource Not Found",
        'tip':"The resource you are trying to access does not exist here",
        'url':"/",
        'action':"Back to Home Page"
    }
    return render_template("error.html",**locals())

@app.errorhandler(405)
def error_405(error):
    error = {
        'title':"Error 405 Occured!",
        'desc':"Method Not Allowed",
        'tip':"The method is not allowed for the requested URL.",
        'url':"/",
        'action':"Back to Home Page"
    }
    return render_template("error.html",**locals())

@app.errorhandler(413)
def no_content_found(error):
    error = {
        'title':"No Data Found",
        'desc':"No Accident Data is found in the system for the specified URI",
        'tip':"Wong Accident Object.",
        'url':"/dashboard",
        'action':"Back to Dashboard"
    }
    return render_template("error.html",**locals())

@app.errorhandler(500)
def error_500(error):
    error = {
        'title':"Server Error 500 Occured",
        'desc':"An Internal Error Occured",
        'tip':"Contact system support unit for assistance on this Erro",
        'url':"/contact",
        "action":"Contact Support Team"
    }
    return render_template("error.html",**locals())