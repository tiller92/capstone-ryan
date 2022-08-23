import os

from unittest import TestCase

from models import db, Users, Watched

os.environ['DATABASE_URL'] = 'postgresql:///cap_test'

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class UserHomeView(TestCase):
  """test that the user log in page loads with user """
  
  def setUp(self):
      db.drop_all()
      db.create_all()
      
      self.client = app.test_client()
      
      self.testuser = Users(username='test', password='1234', email='test@gmail.com')
      id = 48484
      self.testuser.id = id
      db.session.add(self.testuser)
      db.session.commit()
      
  def testHome(self):
    """Test Home page with no User"""
    with self.client as c:
      res = c.get('/')
      print(res)
      self.assertEqual(res.status_code, 200)
      
  def testUserHome(self):
    """Test Home page with user. Should redirect """
    with self.client as c:
      with c.session_transaction() as sess:
        sess[CURR_USER_KEY] = self.testuser.id
    with self.client as c:
      res = c.get('/')
      print(res)
      self.assertEqual(res.status_code, 200)
      
        
  
  def testAddCongressman(self):
    """test the sign up view """
    membername = 'Hon. John Rutherford'
    with self.client as c:
        c.post(f'/users/test')
        
    res = c.post(f'/api/add/watched/test/{membername}') 
    self.assertEqual(res.status_code,302)
    
  
  
  
      