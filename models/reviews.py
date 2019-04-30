from . import db
import datetime
from marshmallow import fields, Schema

class ReviewsModel(db.Model):
    """
        Reviews Models
    """ 
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    kontrol_condition = db.Column(db.String(50), nullable=False)
    review_details = db.Column(db.Text,nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    kontrol_id = db.Column(db.Integer(), db.ForeignKey('kontrols.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('users.u_id'))
    kontrol_foto = db.Column(db.Text,nullable=True)

    def __init__(self, data): 
        self.user_id = data.get('user_id') 
        self.kontrol_id = data.get('kontrol_id') 
        self.kontrol_condition = data.get('kontrol_condition') 
        self.review_details = data.get('review_details') 
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()
        self.kontrol_foto = data.get('kontrol_foto')

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
    def get_reviews_from_db():
        return ReviewsModel.query.all()
    @staticmethod
    def get_one_review(id):
        return ReviewsModel.query.get(id)

    @staticmethod
    def get_review_of(user_id):
        return ReviewsModel.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_kontrol_reviews(kontrol_id):
        return ReviewsModel.query.filter_by(kontrol_id=kontrol_id).all()


    def __repr__(self):
        return '<id {}>'.format(self.id)

class ReviewsModelSchema(Schema):
    """
    ReviewsModel Schema
    """
    id = fields.Int(dump_only=True)
    kontrol_condition = fields.Str(required=True)
    review_details = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True) 
    modified_at = fields.DateTime(dump_only=True) 
    kontrol_id = fields.Int()
    user_id = fields.Int()
    kontrol_foto = fields.Str()