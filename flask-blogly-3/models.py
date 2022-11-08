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

  tags = db.relationship('PostTag', backref='post')

  def print(self):
    print(self.title)
    print(self.content)
    print(self.user)

  def remove(self):
    db.session.delete(self)
    db.session.commit()
  
  def edit(self, title, content, tags):
    self.title = title
    self.content = content
    # Delete old tags first
    for tag in self.tags:
      db.session.delete(tag)
      db.session.commit()
    # Put new tags in
    self.tags = tags
    db.session.add(self)
    db.session.commit()

class Tag(db.Model):
  """Tags"""

  __tablename__ = 'tags'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)

  name = db.Column(db.String(50), nullable=False)

  posts = db.relationship('PostTag', backref='tag')

  def remove(self):
    db.session.delete(self)
    db.session.commit()
  
  def edit(self, name):
    self.name = name
    db.session.add(self)
    db.session.commit()

class PostTag(db.Model):
  """Tags for posts"""

  __tablename__ = 'posts_tags'

  post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)

  tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

  def remove(self):
    db.session.delete(self)
    db.session.commit()