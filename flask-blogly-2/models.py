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


class Post(db.Model):
  """Posts"""

  __tablename__ = 'posts'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)

  title = db.Column(db.String(30), nullable=False)

  content = db.Column(db.String(300), nullable=False)

  created_at = db.Column(db.DateTime, server_default=db.func.now())

  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

  user = db.relationship('User', backref='posts')

  def print(self):
    print(self.title)
    print(self.content)
    print(self.user)

  def remove(self):
    db.session.delete(self)
    db.session.commit()
  
  def edit(self, title, content):
    self.title = title
    self.content = content
    db.session.add(self)
    db.session.commit()
