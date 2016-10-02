from Database import db

class Product(db.Model):
  uuid = db.Column(db.String(36), unique=True, primary_key=True)
  email = db.Column(db.String(128), unique=True)

  def __init__(self, uuid, email):
    self.uuid = uuid;
    self.email = email
