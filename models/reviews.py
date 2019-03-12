from . import db
import datetime
from marshmallow import fields, Schema

class ReviewsModel(db.Model):
    """
        Reviews Models
    """ 
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    reviewed_by = db.Column(db.String(128), nullable=False)
    review_for = db.Column(db.String(128), nullable=False)
    kontrol_condition = db.Column(db.String(128), nullable=False)
    review_details = db.Column(db.Text,nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    reviews = db.relationship('UserModel', backref='reviews', lazy=True)

    def __init__(self, data): 
        self.reviewed_by = data.get('reviewed_by') 
        self.review_for = data.get('review_for') 
        self.kontrol_condition = data.get('kontrol_condition') 
        self.review_details = data.get('review_details') 
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
    def get_reviews_from_db():
        return ReviewsModel.query.all()
    @staticmethod
    def get_one_review(id):
        return ReviewsModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class ReviewsModelSchema(Schema):
    """
    ReviewsModel Schema
    """
    id = fields.Int(dump_only=True)
    reviewed_by = fields.Str(required=True)
    review_for = fields.Str(required=True)
    kontrol_condition = fields.Str(required=True)
    review_details = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True) 
    modified_at = fields.DateTime(dump_only=True) 