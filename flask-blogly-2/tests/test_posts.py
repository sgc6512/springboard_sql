from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URL'] = 'postgresql:///blogly_test'

app.config['TESTING'] = True

with app.app_context():
  db.drop_all()
  db.create_all()

class PostViewsTestCase(TestCase):
  """Test list of users"""

  def setUp(self):
    """Add test user and post"""
    with app.app_context():
      Post.query.delete()
      User.query.delete()

      user = User(first_name="test", last_name="user", image_url="")
      db.session.add(user)
      db.session.commit()

      post = Post(title="Post title", content="Post content", user_id=user.id)
      db.session.add(post)
      db.session.commit()

      self.user_id = user.id
      self.post_id = post.id

  def tearDown(self):
    with app.app_context():
      db.session.rollback()

  def test_list_posts(self):
    """Check to be posts are listed on page"""
    with app.test_client() as client:
      resp = client.get(f"/users/{self.user_id}")
      html = resp.get_data(as_text=True)

      self.assertEqual(resp.status_code, 200)
      self.assertIn('Post title', html)

  def test_posts_details(self):
    """Test to see if post details page comes up"""
    with app.test_client() as client:
      resp = client.get(f"/posts/{self.post_id}")
      html = resp.get_data(as_text=True)

      self.assertEqual(resp.status_code, 200)
      self.assertIn('Post content', html)
  
class PostFormsTestCase(TestCase):

  def setUp(self):
    """Add test user and post"""
    with app.app_context():
      Post.query.delete()
      User.query.delete()

      user = User(first_name="test", last_name="user", image_url="")
      db.session.add(user)
      db.session.commit()

      post = Post(title="Post title", content="Post content", user_id=user.id)
      db.session.add(post)
      db.session.commit()

      self.user_id = user.id
      self.post_id = post.id

  def tearDown(self):
    with app.app_context():
      db.session.rollback()
  
  def test_post_add_form(self):
    """Test to see if form for adding new users comes up"""
    with app.test_client() as client:
      resp = client.get(f"/users/{self.user_id}/posts/new")
      html = resp.get_data(as_text=True)

      self.assertEqual(resp.status_code, 200)
      self.assertIn('<h1>Add Post for test user</h1>', html)
  
  def test_add_post(self):
    """Test to see if adding a new user works"""
    with app.test_client() as client:
      d = {"title": "Test Post 2", "content": "Test Content 2", "user_id":"1"}
      resp = client.post(f"/users/{self.user_id}/posts/new", data=d, follow_redirects=True)
      html = resp.get_data(as_text=True)

      self.assertEqual(resp.status_code, 200)
      self.assertIn('Test Post 2', html)

