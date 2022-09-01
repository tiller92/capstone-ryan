import email
from models import *
from app import app


db.create_all()


user_one = Users(username='ryry', email='till@gmail.com', password='1234')


db.session.add(user_one)
db.session.commit()

