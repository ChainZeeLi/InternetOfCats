from flask import Flask, request
from werkzeug import secure_filename
import os
import ipfsapi
import mysql.connector
import subprocess


UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = set(['jpg','png'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '.'


@app.route('/upload', methods=['POST'])
def upload():
	if request.method == 'POST':
		file = request.files['file']
		if file:
			# save file to current directory
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

			# save file to IPFS 
			api = ipfsapi.connect('127.0.0.1', 5001)
			res = api.add(filename)

			# update database 
			Hash = res['Hash']
			File_name = res['Name']
			mydb = mysql.connector.connect( host="localhost",user="root",passwd="Mark1234",db="image_db")
			mycursor = mydb.cursor()
			mycursor.execute("CREATE TABLE IF NOT EXISTS images(file_name VARCHAR(255), hash VARCHAR(255) );")
			sql = "INSERT INTO images (file_name, hash) VALUES (%s, %s)"
			val = (File_name, Hash)
			mycursor.execute(sql, val)
			mydb.commit()

			# delete file to save memory
			subprocess.call(["rm", filename])
			print res
	return ""


@app.route('/retrieve', methods=['GET'])
def get_all_files():
	if request.method == 'GET':

		f=open(file_name,"w+")
		image = api.cat(Hash);
		f.write(image)
		f.close()

		data = {'file': open(Name, 'rb'), 'modelId': ('', '28343a90-1026-4fd4-835d-01fc684547f0'). }
		headers = {'accept': 'application/x-www-form-urlencoded'}

	return ""



@app.route('/classify', methods=['GET'])
def classify_image():
	return ""









