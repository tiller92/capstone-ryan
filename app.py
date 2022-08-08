from base64 import encode
from crypt import methods
from forms import UserLogin, SignUpForm
import os
from urllib import response
import requests
from flask import Flask, render_template, request, flash, redirect, session, g,json
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import bcrypt
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

CURR_USER_KEY = "curr_user"

## user state
@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = Users.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def login_user(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def logout_user():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


############################### Home Pag, Login and Sign Up routes ##############
@app.route('/', methods=["GET", "POST"])
def home_page():
    users = Users.query.all()
    form = UserLogin()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.data['username']).first_or_404()
        password = form.data['password'].encode('utf-8')
        hashed = user.password.encode('utf-8')
        print(password, hashed)
        if bcrypt.checkpw(password, hashed):
            login_user(user)
            print('user logged in')
            return redirect(f'/users/{user.username}')
        else:
            print('wrong password')
    return render_template('home.html', form=form)


@app.route('/signup', methods=["GET","POST"])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit() and request.method == "POST":
        password = form.data['password']
        # work factor defaults to 12
        hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        # update db with user and user info
        new_user = Users(username=form.data['username'],password=hashed_pwd.decode('utf-8'),email=form.data['email'])
        db.session.add(new_user)
        db.session.commit()
        username = form.data['username']
        flash('New User Created')
        return redirect(f'/users/{username}')
    return render_template('signup.html', form=form)
    

############################### User Routes #################
@app.route('/users/<username>' ,methods=['POST', 'GET'])
def user_page(username):
    print(username, 'username')
    return render_template('/users/userHome.html', username=username)




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


@app.route('/logout')
def logout():
    logout_user()
    flash('You Logged out')
    return redirect('/')


#################### test routes #############

@app.route('/listofusers', methods=["GET"])
def users():
    list_of_users = Users.query.all()
    print(list_of_users)
    return f'{len(list_of_users)}'