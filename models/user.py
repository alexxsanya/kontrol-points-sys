from . import db
import datetime
from marshmallow import fields, Schema

class UserModel(db.Model):
    """
        Users Models
    """ 
    __tablename__ = 'users'

    u_id = db.Column(db.Integer, primary_key=True)
    u_firstname = db.Column(db.String(30), nullable=False)
    u_lastname = db.Column(db.String(30), nullable=False)
    u_telephone = db.Column(db.String(15), nullable=False, unique=True)
    u_email = db.Column(db.String(35),nullable=False, unique=True)
    u_password = db.Column(db.String(150), nullable=False)
    u_role = db.Column(db.String(15), default='user')
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    kontrols= db.relationship('KontrolsModel', backref='users')

    def __init__(self, data):  
        self.u_firstname = data.get('u_firstname') 
        self.u_lastname = data.get('u_lastname') 
        self.u_telephone = data.get('u_telephone') 
        self.u_email = data.get('u_email') 
        self.u_password = data.get('u_password') 
        self.u_role = data.get('u_role') 
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_users_from_db():
        return UserModel.query.all()
    @staticmethod
    def get_one_user(id):
        return UserModel.query.get(id)
    @staticmethod
    def get_user_by_email(email): 
        return UserModel.query.filter_by(u_email=email).first()
    def __repr__(self):
        return '<id {}>'.format(self.id)

class UserModelSchema(Schema):
    """
    UserModel Schema 
    """
    
    u_id = fields.Int(dump_only=True)
    u_firstname = fields.Str(required=True)
    u_lastname = fields.Str(required=True)
    u_telephone = fields.Str(required=True)
    u_email = fields.Str(required=True)
    u_password = fields.Str(required=True)
    u_role = fields.Str()
    created_at = fields.DateTime(dump_only=True) 
    modified_at = fields.DateTime(dump_only=True) 