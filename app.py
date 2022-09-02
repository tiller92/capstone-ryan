from forms import AddWatched, UserLogin, SignUpForm
import os
import requests
from flask import Flask, render_template, request, flash, redirect, session, g,json
from flask_bcrypt import bcrypt
from models import db, connect_db, Users,Transactions,Watched
from helpers import transactions,search_by_name, filterByTransactionDate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URL'] = (
    os.environ.get('DATABASE_URL', 'postgresql://ozytcibgghcnrf:66bd9f09f87426a91c9a08b1383a614aa47ea03f51f0f7d11f38618dc7362554@ec2-44-207-126-176.compute-1.amazonaws.com:5432/d70m2kn71hnkrg'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "secret")

connect_db(app)

CURR_USER_KEY = "curr_user"

## user state
@app.before_request
def add_user_to_g():
    """If logged in, add curr user to Flask global."""
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
    form = UserLogin()
    
    if form.validate_on_submit():
        try:
            user = Users.query.filter_by(username=form.data['username']).first_or_404()
            password = form.data['password'].encode('utf-8')
            hashed = user.password.encode('utf-8')
            if bcrypt.checkpw(password, hashed):
                login_user(user)
                return redirect(f'/users/{user.username}')
            else:
                return redirect('/')
        except:
            print('try failed')
            return redirect('/')
    return render_template('home.html', form=form)


@app.route('/signup', methods=["GET","POST"])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit() and request.method == "POST":
        try:
            password = form.data['password']
        # work factor defaults to 12
            hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        # update db with user and user info
            new_user = Users(username=form.data['username'],password=hashed_pwd.decode('utf-8'),email=form.data['email'])
            db.session.add(new_user)
            db.session.commit()
            username = form.data['username']
            return redirect(f'/users/{username}')
        except:
            ## should probably flash an error here
            flash('username already exists')
            redirect('/signup')
    return render_template('signup.html', form=form)
    

############################### User Routes AND CRUD  #################
@app.route('/users/<username>' ,methods=['POST', 'GET'])
def user_page(username):
    form = AddWatched()
    u = Users.query.filter_by(username=username).first_or_404()
    w = Watched.query.filter_by(user_id=u.id).all()
    if form.validate_on_submit() and request.method == "POST":
        first_name = form.data['first_name']
        last_name = form.data['last_name']
        reps = search_by_name(first_name, last_name)
        db.session.commit()
        return render_template('/users/userHome.html', username=username,form=form, reps=reps,watched_list=w)
    db.session.commit()
    return render_template('/users/userHome.html', username=username,form=form, watched_list=w)

@app.route('/<username>/<rep>/trans',methods=['GET','POST'])
def show_tran(username,rep):
    """Needs to return a list of transactions."""
    trans = transactions()
    trans_list = []
    for tran in trans:
        if rep in tran['representative']:
                trans_list.append(tran)
    ## if user wants filter time complexity moves from o(n) to o(n^6)
    if request.args.get('filter'): 
        filter_trans = filterByTransactionDate(trans_list)
        return render_template('/users/trans.html', trans_list=filter_trans,rep=rep,username=username)
    else:
        return render_template('/users/trans.html', trans_list=trans_list,rep=rep,username=username)


@app.route('/<username>/<rep>/delete', methods=['DELETE',"GET"])
def delete_from_db(username,rep):
    """deletes from DB"""
    user= Users.query.filter_by(username=username).first_or_404()
    w = Watched.query.filter_by(name=rep,user_id=user.id).first_or_404()
    db.session.delete(w)
    db.session.commit()
    return redirect(f'/users/{username}')

@app.route('/logout')
def logout():
    logout_user()
    flash('You Logged out')
    return redirect('/')

################### consumable API routes here ##############
@app.route('/api/stockwatcher')
def api_call():
   # test api calls
    # > 1400 items when called so call as few times as possible
    res_trans = requests.get('https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/all_transactions.json')
    ## this call is no working error 403
    res_data = requests.get('https://house-stock-watcher-data.s3-us-west-2.amazonaws.com')
    transactions = res_trans.text
    trans_dict = json.loads(transactions)
    return 

@app.route('/api/add/watched/<username>/<rep>', methods=["Get", "POST"])
def add_to_watch(username,rep):
    """upated users watched list"""
    info = rep
    ## would be better if you already had the user ID
    user = Users.query.filter_by(username=username).first_or_404()
    new_watched = Watched(name=info,user_id=user.id)
    try:
        db.session.add(new_watched)
        db.session.commit()
    except:
        print('somthing went wrong')
    return redirect(f'/users/{username}')


#################### test routes #############

@app.route('/listofusers', methods=["GET"])
def users():
    list_of_users = Users.query.all()
    print(list_of_users)
    return f'{len(list_of_users)}'