from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from pymongo import MongoClient
import bcrypt
import os

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'db_web_social'
app.config["MONGO_URI"] = "mongodb://localhost:27017/db_web_social"
#"mongodb+srv://tiago:Ribeiro83@@cluster0-kwb0e.azure.mongodb.net/db_web_social" 

mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        return 'Você está logado como ' + session['username']

    return render_template('login.html')

@app.route('/profile')
def profile():
    user_profile = mongo.db.users.find({'username': session['username']})
    return render_template('profile.html',users=user_profile)

@app.route('/user_suggestion')
def suggestion():
    user_suggestion = mongo.db.users.find({'username': session['username']})
    return render_template('home.html',users=user_suggestion)

@app.route('/home')
def home():
    user = mongo.db.users.find()
    post = mongo.db.posted.find()
    return render_template('home.html',users=user,posted=post)

@app.route('/user_number')
def user_number():
    user_number = mongo.db.users.find()
    user_number_count = user_number.count(True)
    return render_template('user_number.html',users=user_number_count)

@app.route('/action', methods=['POST'])
def action():

    if request.method == 'POST':
        posted = mongo.db.posted
        existing_posted = posted.find_one({'posted' : request.form['post']})

        if existing_posted is None:
            posted.insert({'username': session['username'], 'posted': request.form['post']})
            return redirect(url_for('home'))

        return 'Essa postagem já existe'
##  <button type="button" class="btn btn-primary">Publicar</button>

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'username': request.form['username']})

    error = None
    if request.method == 'POST':
        if request.form['username'] != login_user['username'] or request.form['password'] != login_user['password']:
            error = ''
        else:
            session['username'] = request.form['username']
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'username' : request.form['username']})

        if existing_user is None:
            #hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name':request.form['nome'], 'username':request.form['username'], 'password': request.form['password'], 'city': request.form['city'], 'state': request.form['state']})
            session['username'] =  request.form['username']
            return redirect(url_for('login'))

        return 'Esse usuário já existe'

    return render_template('register.html')

#@app.route("/logout")
#@login_required
#def logout():
#  logout_user()
#  return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.secret_key = "senhasecreta"
    #app.run(threaded=True, port=5000)
    app.run(debug=True)