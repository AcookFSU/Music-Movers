import mysql.connector
import datetime

username = ''
password = ''
if not username:
    print("Enter username for local MySQL installation")
    username = input()
if not password:
    print("Enter password for local MySQL installation")
    password = input()

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user=username,
    password=password,
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS musicMovers")
mycursor.execute("USE musicMovers")
mycursor.execute("CREATE TABLE IF NOT EXISTS users (userId INT AUTO_INCREMENT PRIMARY KEY, username TEXT UNIQUE, password CHAR(64), joinDate DATE, userType TEXT, userScore INT)")
mycursor.execute("CREATE TABLE IF NOT EXISTS songs (songId INT AUTO_INCREMENT PRIMARY KEY, name TEXT, artistUserId INT , lyrics LONGTEXT)")
mycursor.execute("CREATE TABLE IF NOT EXISTS posts (postId INT AUTO_INCREMENT PRIMARY KEY, songId INT NOT NULL, authorUserId INT NOT NULL, interp TEXT, postScore INT)")
mydb.commit()

mycursor.execute("CREATE ROLE IF NOT EXISTS admin")
mycursor.execute("CREATE ROLE IF NOT EXISTS editor")
mycursor.execute("CREATE ROLE IF NOT EXISTS viewer")

mycursor.execute("GRANT ALL PRIVILEGES ON musicMovers.* TO 'admin'")
#mycursor.execute("GRANT SELECT, INSERT, UPDATE ON musicMovers.* TO 'editor'")
#mycursor.execute("GRANT SELECT ON musicMovers.* TO 'viewer'")

mycursor.execute("CREATE USER IF NOT EXISTS 'testuser'@'localhost' IDENTIFIED BY 'password'")
mycursor.execute("GRANT 'admin' TO 'testuser'@'localhost'")
mycursor.execute("SET DEFAULT ROLE 'admin' TO 'testuser'@'localhost';")

mycursor.execute("FLUSH PRIVILEGES")

mydb.commit()
print("Succesfully setup music movers and created roles with permissions!")

