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
mycursor.execute("CREATE TABLE IF NOT EXISTS users (userId INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(30) UNIQUE, password CHAR(64) NOT NULL, joinDate DATE, userType VARCHAR(15) NOT NULL)")
mycursor.execute("CREATE TABLE IF NOT EXISTS songs (songId INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50), artistUserId INT NOT NULL, lyrics LONGTEXT)")
mycursor.execute("CREATE TABLE IF NOT EXISTS posts (postId INT AUTO_INCREMENT PRIMARY KEY, songId INT NOT NULL, authorUserId INT NOT NULL, interp TEXT)")
mydb.commit()

mycursor.execute("CREATE ROLE IF NOT EXISTS viewer")
mycursor.execute("CREATE ROLE IF NOT EXISTS acctManager")

mycursor.execute("GRANT SELECT ON musicMovers.songs TO 'viewer'")
mycursor.execute("GRANT SELECT, INSERT ON musicMovers.posts TO 'viewer'")
mycursor.execute("GRANT CREATE USER ON *.* TO 'acctManager'") #new
mycursor.execute("GRANT SELECT, INSERT ON musicMovers.users TO 'acctManager'")
mycursor.execute("GRANT 'viewer' to 'acctManager'@'localhost' WITH ADMIN OPTION")# new

mycursor.execute("CREATE USER IF NOT EXISTS 'acctManager'@'localhost' IDENTIFIED BY 'COP4521DBAdminPassword'")
mycursor.execute("GRANT 'acctManager' TO 'acctManager'@'localhost'")
mycursor.execute("SET DEFAULT ROLE 'acctManager' TO 'acctManager'@'localhost';")

mycursor.execute("FLUSH PRIVILEGES")

mydb.commit()
print("Succesfully setup music movers and created roles with permissions!")

