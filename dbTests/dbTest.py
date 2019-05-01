import mysql.connector


mydb = mysql.connector.connect( host="localhost",user="root",passwd="Mark1234",db="image_db")
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS images3(file_name VARCHAR(255), hash VARCHAR(255), detection_score FLOAT(24), classification_score FLOAT(24) );")


sql = "INSERT INTO images3(file_name, hash, detection_score) VALUES (%s, %s, %s)"
val = ("cat88.jpg", "12334345", "0.999")
mycursor.execute(sql, val)
mydb.commit()


sql = "INSERT INTO images3(file_name, hash, detection_score) VALUES (%s, %s, %s)"
val = ("cat81.jpg", "123343das", "0.9999")
mycursor.execute(sql, val)
mydb.commit()


"""
mycursor.execute("SELECT * FROM images3")
result_set = mycursor.fetchall()
for row in result_set:
	file_name = row[0]
	Hash = row[1]
	SCORE = row[2]
	print (file_name,Hash,SCORE)
"""


sql="SELECT file_name, Hash FROM images3"
#sql="DELETE FROM images3 WHERE detection_score>1"
mycursor.execute(sql)
result_set = mycursor.fetchall()
print str(result_set[0][0])

