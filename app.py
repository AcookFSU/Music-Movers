import os
from urllib import request

from flask import Flask, render_template, request # type: ignore
from werkzeug.utils import secure_filename
import flask_login
import datetime


#SETUP FLASK
import mysql.connector
app = Flask(__name__)
app.secret_key = '449259b0c773e49eb92c45cc34ffee5bb0b4b979f38b1b7d10531194b02f9086'
app.config['UPLOAD_FOLDER'] = '/path/to/upload/directory'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    username = ""
    password = ""
    pass

#ROUTES

@login_manager.user_loader
def load_user(user_id):
    mydb = mysql.connector.connect(host="localhost", user="acctManager", password="COP4521DBAdminPassword", database="musicMovers")
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT userId, username, password from users WHERE userId = '{user_id}'")
    user = User()
    query = mycursor.fetchone()
    if query:
        user.id = query[0]
        user.username = query[1]
        user.username = query[2]
    return user

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/test')#DELETE BEFORE PRODUCTION IMPORTANT DONT FORGET
def test():
    print(flask_login.current_user.id)
    return render_template('index.html')

@app.route('/search')
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
            user="acctManager",
            password="COP4521DBAdminPassword",
            database="musicMovers"
        )
        mycursor = mydb.cursor() #Add error handling later
        mycursor.execute("INSERT INTO users (username, password, joinDate, userType) VALUES (%s,%s,%s,%s)", (uname, pword, datetime.date.today(), "listener"))
        mycursor.execute(f"CREATE USER IF NOT EXISTS '{uname}'@'localhost' IDENTIFIED BY '{pword}'")
        mycursor.execute(f"GRANT 'viewer' TO '{uname}'@'localhost'")
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
        pword = request.form['password']
        mydb = mysql.connector.connect(host="localhost", user="acctManager", password="COP4521DBAdminPassword", database="musicMovers")
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT userId from USERS where username = '{uname}' and password = '{pword}'")
        query = mycursor.fetchone()
        if query:
            print('Login succesful')
            user = User()
            user.id = query[0]
            flask_login.login_user(user)
            return render_template('index.html')
        else:
            print('Login unsuccesful')
            return render_template('login.html')


@app.route('/song/<songid>')
def song(songid):
    #more here
    #SELECT username, interp from posts INNER JOIN users ON users.userId = posts.authorUserId WHERE posts.songId = '{songId}'
    #SELECT username, songs.name, lyrics from songs INNER JOIN users ON artistUserId = users.userId WHERE songId = '{songId}'
    mydb = mysql.connector.connect(
        host="localhost",
        user=flask_login.current_user.username,
        password=flask_login.current_user.password,
        database="musicMovers"
    )
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(f"SELECT username, songs.name, lyrics from songs INNER JOIN users ON artistUserId = users.userId WHERE songId = '{songid}'")
    song = mycursor.fetchone()
    print(song)
    mycursor.execute(f"SELECT username, interp from posts INNER JOIN users ON users.userId = posts.authorUserId WHERE posts.songId = '{songid}'")
    rows=mycursor.fetchall()
    print(rows)
    mycursor.close()
    mydb.close()
    return render_template('song.html', song=song, rows=rows)
@app.route('/interpPost/<songid>', methods = ['GET', 'POST'])
def interpPost(songId):
    thetext = request.form['thetext']
    mydb = mysql.connector.connect()
    mycursor = mydb.cursor()
    mycursor.execute("INSERT INTO posts (interp, songId, authorUserId, postScore) VALUES (%s,%s, %s, %s)", (thetext, songId, flask_login.current_user.id ,0))
@app.route('/songResults', methods = ['GET', 'POST'])
def list_songs():
    search = request.form['f']

    mydb = mysql.connector.connect(
        host="localhost",
        user=flask_login.current_user.username,
        password=flask_login.current_user.password,
        database="musicMovers"
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