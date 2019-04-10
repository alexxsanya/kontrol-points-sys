from flask import (Flask, 
                    render_template, 
                    jsonify, flash, 
                    redirect, url_for, request, 
                    Response,session,abort,
                    send_from_directory)
import json,os
from werkzeug import secure_filename
from flask import Flask
from models import db, bcrypt
import config
from os import environ
from flask_bootstrap import Bootstrap
from models.controls import KontrolsModel,KontrolsModelSchema
from models.reviews import ReviewsModel,ReviewsModelSchema
from models.user import UserModel,UserModelSchema

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

@app.route('/create-user', methods=['POST'])
def create_user():
    req_data = request.form.to_dict(flat=True)

    req_data['u_role'] = 'user'

    data, error = UserModelSchema().load(req_data)

    if error:
        return json.dumps(error)
    user_in_db = UserModel.get_user_by_email(data.get('u_email'))
    if user_in_db:
        message = 'User already exist with supplied email address'
        flash(message,'error')        
        return redirect(url_for('home'))

    user = UserModel(data)
    user.save()

    user_data = UserModelSchema().dump(user).data
    message = "Account Created, Now Login"
    flash(message,'success')        
    return redirect(url_for('home'))

@app.route('/login-user', methods=['POST'])
def login_user():
    user = request.form.to_dict(flat=True)  

    user = UserModel.get_user_by_email(user.get('l_email'))    
    
    user = UserModelSchema().dump(user).data  

    if user != {} and '@' in str(user.get('u_email')):
        session['username'] = user.get('u_email')
        session['user_id'] = user.get('u_id')

        flash('You are successfully logged in','success')

        return redirect(url_for('home'))

    else: 

        flash('Logged in with wrong credentials','error')

        return redirect(url_for('home'))

@app.route('/logout-user')
def logout_user():
    session.pop("username",None)
    session.pop("user_id",None)
    flash('You are successfully logged out','success')
    return redirect(url_for('home'))

@app.route('/create-point',methods=['POST'])
def create_point():
    req_data = request.form.to_dict(flat=True)

    req_data['k_utm'] = req_data.get('k_utm_n') + ',' + req_data.get('k_utm_e')\
        + ',' + req_data.get('k_utm_h')

    req_data['k_geocord'] = req_data.get('k_geo_lat')+ ',' + req_data.get('k_geo_lng')
    req_data['user_id'] = int(req_data.get('k_created_by'))
    data, error = KontrolsModelSchema().load(req_data)

    if error:
        return json.dumps(error)
    point_in_db = KontrolsModel.get_kontol_by_name(req_data.get('k_name'))
    if point_in_db:
        message = 'Control Point Already Recorded'
        flash(message,'error')        
        return redirect(url_for('home'))

    kpoint = KontrolsModel(data)
    kpoint.save()

    user_data = KontrolsModelSchema().dump(kpoint).data
    message = "Control Point has been successfully created"
    flash(message,'success')        
    return redirect(url_for('home'))

@app.route('/update-point',methods=['POST'])
def update_point():
    req_data = request.form.to_dict(flat=True)

    req_data['k_utm'] = req_data.get('k_utm_n') + ',' + req_data.get('k_utm_e')\
        + ',' + req_data.get('k_utm_h')

    req_data['k_geocord'] = req_data.get('k_geo_lat')+ ',' + req_data.get('k_geo_lng')
    req_data['user_id'] = int(req_data.get('k_created_by'))
    data, error = KontrolsModelSchema().load(req_data)

    if error:
        return json.dumps(error)
    point_in_db = KontrolsModel.get_kontol_by_name(data.get('k_name'))

    if point_in_db:
        kpoint = KontrolsModel(data)
        kpoint.update(data)

        user_data = KontrolsModelSchema().dump(kpoint).data
        print(user_data)
        message = "Control Point Updated successfully"
        flash(message,'success')        
        return redirect(url_for('get_points',point_name=req_data['k_name']))
    else:
        message = 'No Control Point In System With Provided Name'
        flash(message,'error')        
        return redirect(url_for('get_points',point_name=req_data['k_name']))

@app.route('/all-points')
def get_all_points():
    kontrols =  KontrolsModel.get_kontrols_from_db() 
    data = KontrolsModelSchema().dump(kontrols, many=True).data 
    return jsonify(data)

@app.route('/points/<string:point_name>')
def get_points(point_name):
    kontrols =  KontrolsModel.get_kontol_by_name(point_name) 

    if not kontrols:
        return jsonify({}) # Using 413 in place of 204 No Content Found

    data = KontrolsModelSchema().dump(kontrols).data 

    reviews = ReviewsModel.get_review_of(data.get('id'))
    review_data = ReviewsModelSchema().dump(reviews, many=True).data 
    #return jsonify(data)
    return render_template("point.html",point=data,reviews=review_data)

@app.route('/assets/<img_uri>')
def get_photo(img_uri): 
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               img_uri)

@app.route('/add-review',methods=['POST'])
def add_review():
    req_data = request.form.to_dict(flat=True)
    kontrol_foto = request.files['kontrol_foto']
    photo_name = kontrol_foto.filename
    req_data['kontrol_foto'] = photo_name
    photo_name = secure_filename(photo_name)

    if allowed_photos(photo_name):
        path = "views/"+os.path.join(app.config['UPLOAD_FOLDER'],photo_name)
        kontrol_foto.save(path)
    
    data, error = ReviewsModelSchema().load(req_data)
    if error:
        message = error
        flash(message,'error')        
        return redirect(url_for('home'))
    
    kpoint_review = ReviewsModel(data)
    kpoint_review.save()

    user_data = ReviewsModelSchema().dump(kpoint_review).data
    message = "Your review has been successfully added"
    flash(message,'success')        
    return redirect(url_for('home'))

@app.route('/point/reviews/<int:id>',methods=['GET'])
def get_point_reviews(id):
    reviews = ReviewsModel.get_review_of(id)
    data = ReviewsModelSchema().dump(reviews, many=True).data 

    return render_template("reviews.html",reviews=data)

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

def allowed_photos(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in config.Config.ALLOWED_EXTENSIONS