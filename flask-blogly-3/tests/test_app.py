from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URL'] = 'postgresql:///blogly_test'

app.config['TESTING'] = True

with app.app_context():
  db.drop_all()
  db.create_all()

class UserViewsTestCase(TestCase):
  """Test list of users"""

  def setUp(self):
    """Add test user"""
    with app.app_context():
      User.query.delete()

      user = User(first_name="test", last_name="user", image_url="")
      db.session.add(user)
      db.session.commit()

      self.user_id = user.id

  def tearDown(self):
    with app.app_context():
      db.session.rollback()

  def test_list_users(self):
    """Check to be users are listed on page"""
    with app.test_client() as client:
      resp = client.get("/users")
      html = resp.get_data(as_text=True)

      self.assertEqual(resp.status_code, 200)
      self.assertIn('test user', html)

  def test_users_details(self):
    """Test to see if user details page comes up"""
    with app.test_client() as client:
      resp = client.get(f"/users/{self.user_id}")
      html = resp.get_data(as_text=True)

      self.assertEqual(resp.status_code, 200)
      self.assertIn('edit', html)
  
class FormsTestCase(TestCase):

  def tearDown(self):
    with app.app_context():
      db.session.rollback()
  
  def test_add_form(self):
    """Test to see if form for adding new users comes up"""
    with app.test_client() as client:
      resp = client.get("/users/new")
      html = resp.get_data(as_text=True)

      self.assertEqual(resp.status_code, 200)
      self.assertIn('<h1>Create a User</h1>', html)
  
  def test_add_user(self):
    """Test to see if adding a new user works"""
    with app.test_client() as client:
      u = {"first_name": "Test User 1", "last_name": "Springboard", "img_url":""}
      resp = client.post("/users/new", data=u, follow_redirects=True)
      html = resp.get_data(as_text=True)

      self.assertEqual(resp.status_code, 200)
      self.assertIn('Springboard', html)

