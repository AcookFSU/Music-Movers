import os
from urllib import request

from flask import Flask, render_template, request, flash # type: ignore
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
    pass

#ROUTES

@login_manager.user_loader
def load_user(user_id):
    print("USER LOADED")
    mydb = mysql.connector.connect(host="localhost", user="testuser", password="password", database="musicMovers")
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT userId from users WHERE userId = '{user_id}'")
    user = User()
    query = mycursor.fetchone()
    if query:
        user.id = query[0]
    return user

@app.route('/')
def home():
    return render_template('index.html')

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
            user="testuser",
            password="password",
            database="musicMovers"
        )
        mycursor = mydb.cursor() #Add error handling later
        mycursor.execute("INSERT INTO users (username, password, joinDate, userType, userScore) VALUES (%s,%s,%s,%s,%s)", (uname, pword, datetime.date.today(), "listener", 0))
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
        mydb = mysql.connector.connect(host="localhost", user="testuser", password="password", database="musicMovers")
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT userId from USERS where username = '{uname}' and password = '{pword}'")
        query = mycursor.fetchone()
        if query:
            flash('Login succesful')
            user = User()
            user.id = query[0]
            flask_login.login_user(user)
            return render_template('index.html')
        else:
            flash('Login unsuccesful')
            return render_template('login.html')
        

@app.route('/song/<songid>')
def song(songid):
    #more here
    #SELECT username, interp from posts INNER JOIN users ON users.userId = posts.authorUserId WHERE posts.songId = '{songId}'
    #SELECT username, songs.name, lyrics from songs INNER JOIN users ON artistUserId = users.userId WHERE songId = '{songId}'
    mydb = mysql.connector.connect(
        host="localhost",
        user="testuser",
        password="password",
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

@app.route('/songResults', methods = ['GET', 'POST'])
def list_songs():
    search = request.form['f']

    mydb = mysql.connector.connect(
        host="localhost",
        user="testuser",
        password="password",
        database="musicMovers"
    )
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(f"SELECT name, username from songs  where name like '%' + search + '%' and artistUserId = userId")
    rows = mycursor.fetchall()
    return render_template('songResults.html', rows=rows, search=search)

@app.route('/upload_profile_picture', methods=['POST'])
def upload_profile_picture():
    if 'profile_picture' not in request.files:
        return 'No file part'
    file = request.files['profile_picture']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File uploaded successfully'

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug = True, port=8000)
