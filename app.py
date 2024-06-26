from urllib import request

from flask import Flask, render_template, request, flash, redirect # type: ignore
from werkzeug.utils import secure_filename
import flask_login
from flask_login import login_required
import datetime
import hashlib

#SETUP FLASK
import mysql.connector
app = Flask(__name__)
app.secret_key = '449259b0c773e49eb92c45cc34ffee5bb0b4b979f38b1b7d10531194b02f9086' #Required for flask_login to work without errors

login_manager = flask_login.LoginManager() #Create the login manager for flask-login 
login_manager.init_app(app)

class User(flask_login.UserMixin): #Use the provided UserMixin class but add fields for username and password so we can use the credential of the logged in users to access the mySql database
    username = ""
    password = ""
    pass

#ROUTES

@login_manager.user_loader #Returns information of a user based on user_id
def load_user(user_id):
    mydb = mysql.connector.connect(host="localhost", user="acctManager", password="COP4521DBAdminPassword", database="musicMovers")
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT userId, username, password from users WHERE userId = '{user_id}'")
    user = User()
    query = mycursor.fetchone()
    
    if query:
        user.id, user.username, user.password = query
    return user

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/user')
def user():
    mydb = mysql.connector.connect(
        host="localhost",
        user=flask_login.current_user.username,
        password=flask_login.current_user.password,
        database="musicMovers"
    )
    username1 = flask_login.current_user.username
    userid = flask_login.current_user.id
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(f"SELECT username, joinDate, userType FROM users WHERE username = '{username1}'")
    user=mycursor.fetchall()
    mycursor.execute(f"SELECT posts.interp, songs.name, posts.songId FROM posts INNER JOIN songs ON posts.songId = songs.songId WHERE posts.authorUserId = '{userid}'")
    interps=mycursor.fetchall()
    mycursor.close()
    mydb.close()
    return render_template('user.html', user=user, interps=interps)

@app.route('/search')
@login_required
def search():
    return render_template('search.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signupprocess', methods = ['GET', 'POST'])
def signupprocess():
    if request.method == 'POST':
        uname = request.form['username']
        pword = request.form['password']
        mydb = mysql.connector.connect( 
            host="localhost",
            user="acctManager",#The account manager is used here to create the user account. We cant use the user's role to connect to db because they dont exist yet
            password="COP4521DBAdminPassword", #Manager only has permission to read users table, grant listener role, and create users
            database="musicMovers",
        )
        mycursor = mydb.cursor()#Setting up the new user
        pword = hashlib.sha256(pword.encode(encoding="ascii")).hexdigest()
        mycursor.execute("INSERT INTO users (username, password, joinDate, userType) VALUES (%s,%s,%s,%s)", (uname, pword, datetime.date.today(), "listener"))
        mycursor.execute(f"CREATE USER IF NOT EXISTS '{uname}'@'localhost' IDENTIFIED WITH caching_sha2_password BY '{pword}'")
        mycursor.execute(f"GRANT 'viewer' TO '{uname}'@'localhost'")
        mycursor.execute(f"SET DEFAULT ROLE 'viewer' TO '{uname}'@'localhost';")
        mycursor.execute("FLUSH PRIVILEGES")
        mydb.commit()
        mycursor.close()
        mydb.close()
        return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/loginprocess', methods = ['GET', 'POST'])
def loginprocess():
    if request.method == 'POST':
        uname = request.form['username']
        pword = request.form['password']#Account manager is used for login here too
        pword = hashlib.sha256(pword.encode(encoding="ascii")).hexdigest()
        mydb = mysql.connector.connect(host="localhost", user="acctManager", password="COP4521DBAdminPassword", database="musicMovers")
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT userId from USERS where username = '{uname}' and password = '{pword}'")
        query = mycursor.fetchone()
        if query:
            flash('Login succesful')
            user = User()
            user.id = query[0]
            flask_login.login_user(user)
            return redirect('/search')
        else:
            flash('Login unsuccesful')
            return redirect('/login')
        

@app.route('/song/<songid>')
@login_required
def song(songid):
    mydb = mysql.connector.connect( #Example of our RBAC
        host="localhost",
        user=flask_login.current_user.username, #Uses the credentials for the logged in user to connect to DBMS, listener role can only select songs, posts, users and insert on posts
        password=flask_login.current_user.password,
        database="musicMovers",
    )
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(f"SELECT songs.songId, username, songs.name, lyrics from songs INNER JOIN users ON artistUserId = users.userId WHERE songId = '{songid}'")
    song = mycursor.fetchone()
    mycursor.execute(f"SELECT username, interp from posts INNER JOIN users ON users.userId = posts.authorUserId WHERE posts.songId = '{songid}'")
    rows=mycursor.fetchall()
    mycursor.close()
    mydb.close()
    return render_template('song.html', song=song, rows=rows)

@app.route('/interpPost', methods = ['GET', 'POST'])
def interpPost():
    songid = request.args.get('songid')
    print(songid)
    thetext = request.form['thetext']
    mydb = mysql.connector.connect(
        host="localhost",
        user=flask_login.current_user.username,
        password=flask_login.current_user.password,
        database="musicMovers",
    )
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("INSERT INTO posts (interp, songId, authorUserId) VALUES (%s,%s, %s)", (thetext, int(songid), flask_login.current_user.id))
    mydb.commit()
    mycursor.close()
    return redirect('/song/' + str(songid))
@app.route('/songResults', methods = ['GET', 'POST'])
@login_required
def list_songs():
    search = request.form['f']

    mydb = mysql.connector.connect(
        host="localhost",
        user=flask_login.current_user.username,
        password=flask_login.current_user.password,
        database="musicMovers",
    )
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(f"SELECT users.username, songs.name, songs.songId from songs INNER JOIN users ON artistUserId = users.userId WHERE name LIKE '%{search}%'")
    rows = mycursor.fetchall()
    mycursor.close()
    mydb.close()

    if not rows:
        error = "No songs found."
        return render_template('searchResults.html', error=error)
    else:
        return render_template('searchResults.html', rows=rows, search=search)


if __name__ == '__main__':
    app.run(debug = True, port=8000)
