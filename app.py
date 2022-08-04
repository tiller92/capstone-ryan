from crypt import methods
from forms import UserLogin
import os
from urllib import response
import requests
from flask import Flask, render_template, request, flash, redirect, session, g,json
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, Users,Transactions,Watched

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///capone'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)
db = SQLAlchemy(app)



## home page will go here
@app.route('/', methods=["GET", "POST"])
def home_page():
    users = Users.query.all()
    print(users[0].watched)
    form = UserLogin()
    if form.validate_on_submit():
        print(form.data)
        
        return redirect('/users/1')
    return render_template('home.html', form=form)
    

## need to make a route that validated the user and then redirects to the user home page
@app.route('/api/validate')
def get_and_validate_user(username):
    print()
    # user = Users.query.filter_by(username=username)
    # print(user)
    
    return redirect('/')

@app.route('/users/<int:user_id>' ,methods=['POST', 'GET'])
def user_page(user_id):
    print(user_id, 'user ID')
    return render_template('/users/userHome.html')

@app.route('/api/stockwatcher')
def api_call():
   # test api calls
    # > 1400 items when called so call as few times as possible
    res_trans = requests.get('https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/all_transactions.json')
    ## this call is no working error 403
    res_data = requests.get('https://house-stock-watcher-data.s3-us-west-2.amazonaws.com')
    transactions = res_trans.text
    trans_dict = json.loads(transactions)
    for i in range(10):
        print(trans_dict[i])
    print(type(trans_dict))
    print(len(trans_dict))
    return 