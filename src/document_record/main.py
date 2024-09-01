import mysql.connector


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="3241",
    auth_plugin='mysql_native_password',
    database="Docmgmt"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM License")

for i in mycursor:
    print(i)
