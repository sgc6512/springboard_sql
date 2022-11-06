from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
  db.app = app
  db.init_app(app)


class User(db.Model):
  """User"""

  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)

  first_name = db.Column(db.String(30), nullable=False)

  last_name = db.Column(db.String(30), nullable=False)

  image_url = db.Column(db.String(50))

  def remove(self):
    db.session.delete(self)
    db.session.commit()
  
  def edit(self, first, last, url):
    self.first_name = first
    self.last_name = last
    self.image_url = url
    db.session.add(self)
    db.session.commit()

