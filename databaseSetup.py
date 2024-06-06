import mysql.connector

username = ''
password = ''
if not username:
    print("Enter username for local MySQL installation")
    username = input()
if not password:
    print("Enter password for local MySQL installation")
    password = input()

mydb = mysql.connector.connect(
    host="localhost",
    user=username,
    password=password,
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS musicMovers")
mycursor.execute("USE musicMovers")
mycursor.execute("CREATE TABLE IF NOT EXISTS users (userId INT AUTO_INCREMENT PRIMARY KEY, username TEXT, password CHAR(64), joinDate DATE, userType TEXT)")
mycursor.execute("CREATE TABLE IF NOT EXISTS songs (songId INT AUTO_INCREMENT PRIMARY KEY, name TEXT, artistUserId INT , lyrics LONGTEXT)")
mycursor.execute("CREATE TABLE IF NOT EXISTS posts (postId INT AUTO_INCREMENT PRIMARY KEY, songId INT NOT NULL, interp TEXT, lineInSong INT)")
