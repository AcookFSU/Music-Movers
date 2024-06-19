import os
from urllib import request

from flask import Flask, render_template, request # type: ignore
from werkzeug.utils import secure_filename
import datetime

import mysql.connector
app = Flask(__name__)

@app.route('/')
def home():
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

@app.route('/login', methods = ['GET', 'POST'])
def login(): #working on
    if request.method == 'POST':
        uname = request.form['username']
        pword = request.form['password']

        # checks for user and if password matches
        if uname in users and users[uname] == pword:
            flash('Login successful')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')

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
        user="testuser",
        password="password",
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