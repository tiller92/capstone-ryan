import os

from unittest import TestCase

from models import db, Users, Watched

os.environ['DATABASE_URL'] = 'postgresql:///cap_test'

from app import app

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class ViewTests(TestCase):
  """ Test to ensure views works and DB connection occurs without error """
  
  def setUp(self):
      db.drop_all()
      db.create_all()
      
      self.client = app.test_client()
      
      self.testuser = Users(username='test', password='1234', email='test@gmail.com')
      self.testuser_id = 1234
      self.testuser.id = self.testuser_id
      db.session.add(self.testuser)
      db.session.commit()
      
      self.watched = Watched(name='Hon. John Rutherford',user_id=self.testuser.id)
      
      db.session.add(self.watched)
      db.session.commit()
      
  def testHome(self):
    """Test Home page with no User"""
    with self.client as c:
      res = c.get('/')
      print(res)
      self.assertEqual(res.status_code, 200)
      
  def testUserHome(self):
    """Test Home page with user"""
    with self.client as c:
      res = c.get('/users/test')
      self.assertEqual(res.status_code, 200)
      
  def testAddCongressman(self):
    """test the sign up view """
    membername = 'Hon. John Rutherford'
    with self.client as c:
        c.post(f'/users/test')
        
    res = c.post(f'/api/add/watched/test/{membername}') 
    self.assertEqual(res.status_code,302)

  def testTransactions(self):
    """Transaction Information Page"""
    membername = 'Hon. John Rutherford'
    with self.client as c:
      res = c.get(f'/test/{membername}/trans')
      
    self.assertEqual(res.status_code, 200)
    
  def testWathcedDelete(self):
    membername = 'Hon. John Rutherford'
    with self.client as c:
      res = c.get('/users/test')
      self.assertEqual(res.status_code, 200)
    
    remove = c.delete(f'/test/{membername}/delete')
    self.assertEqual(remove.status_code, 302)
    
    


  
  
      