import pymysql
db = pymysql.connect(host = "localhost", user = "binod", password = "mysql")
mycur = db.cursor()
# mycur.execute("create database restaurantdb;")
mycur.execute("use restaurantdb;")
mycur.execute("create table ordersfood (RELNUM INT, FoodID CHAR(20), OrderId INT);")
# # mycur.execute("desc menu;")
# mycur.execute("INSERT INTO menu VALUES (1,'Pasta',22.20)")
# mycur.execute("INSERT INTO menu VALUES (2,'Pasta',22.20)")
db.commit()

# a = mycur.execute("select * from menu;")
# a = R=mycur.fetchall()
# print(a)