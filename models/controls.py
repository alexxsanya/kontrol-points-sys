from . import db
import datetime
from marshmallow import fields, Schema

class KontrolsModel(db.Model):
  """
  Kontrol Points Models
  """ 
  __tablename__ = 'kontrols'

  id = db.Column(db.Integer, primary_key=True)
  k_name = db.Column(db.String(50), nullable=False, unique=True)
  k_utm = db.Column(db.String(50), nullable=False)
  k_geocord = db.Column(db.String(50),unique=True)
  k_addr_district = db.Column(db.String(25), nullable=False)
  k_addr_county = db.Column(db.String(50))
  k_addr_subcounty = db.Column(db.String(50), nullable=False) 
  k_method_of_fixation = db.Column(db.String(50),nullable=True) 
  k_equip_used = db.Column(db.String(50), nullable=False)
  k_surveyor = db.Column(db.String(50), nullable=True)
  k_description = db.Column(db.Text,nullable=False)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)
  user_id = db.Column(db.Integer(), db.ForeignKey('users.u_id'))
  reviews = db.relationship('ReviewsModel', backref='kontrols')

  def __init__(self, data):
    self.k_name = data.get('k_name') 
    self.k_utm = data.get('k_utm') 
    self.user_id = data.get('k_created_by') 
    self.k_geocord = data.get('k_geocord') 
    self.k_addr_district = data.get('k_addr_district') 
    self.k_addr_county = data.get('k_addr_county') 
    self.k_addr_subcounty = data.get('k_addr_subcounty') 
    self.k_method_of_fixation = data.get('k_method_of_fixation') 
    self.k_equip_used = data.get('k_equip_used') 
    self.k_surveyor = data.get('k_surveyor') 
    self.k_description = data.get('k_description') 
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
  def get_kontrols_from_db():
    return KontrolsModel.query.all()
  @staticmethod
  def get_one_kontrol(id):
    return KontrolsModel.query.get(id)
  
  @staticmethod
  def get_kontol_by_name(name):
    return KontrolsModel.query.filter_by(k_name=name).first()

  def __repr__(self):
    return '<id {}>'.format(self.id)

class KontrolsModelSchema(Schema):
  """
  KontrolsModel Schema
  """
  id = fields.Int(dump_only=True)
  k_name = fields.Str(required=True)
  k_utm = fields.Str(required=True)
  k_geocord = fields.Str(required=True)
  k_addr_district = fields.Str(required=True)
  k_addr_county = fields.Str(required=True)
  k_addr_subcounty = fields.Str(required=True)
  k_method_of_fixation = fields.Str(required=True)
  k_equip_used = fields.Str(required=True)
  k_surveyor = fields.Str()
  k_description = fields.Str(required=True)
  created_at = fields.DateTime(dump_only=True) 
  modified_at = fields.DateTime(dump_only=True) 
  user_id = fields.Int(dump_only=True)