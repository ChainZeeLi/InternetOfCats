#!/usr/bin/python3
from flask import Flask, request
import flask
from werkzeug import secure_filename
import os
import ipfsapi
from timeit import default_timer
import subprocess
import ast
import requests
import pymysql as mysql
import asyncio
from concurrent.futures import ThreadPoolExecutor


UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = set(['jpg','png'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '../catpix/'
app.config['DATABASE_TABLE'] = 'images3' 
 


@app.route('/upload', methods=['POST'])
def upload():
	mydb,mycursor = db()
	initalize_db();
	File_name=""
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
			#mydb = mysql.connect( host="localhost",user="root",passwd="Mark1234",db="image_db")
			#mycursor = mydb.cursor()
			mycursor.execute("CREATE TABLE IF NOT EXISTS images3(file_name VARCHAR(255), hash VARCHAR(255), detection_score FLOAT(24), classification_score FLOAT(24) );")
			sql = "INSERT INTO images3(file_name, hash) VALUES (%s, %s)"
			val = (File_name, Hash)
			mycursor.execute(sql, val)
			mydb.commit()
			# delete file to save memory
			subprocess.call(["rm", filename])
			#print(res)
	return "Succussfully Uploaded %s"%File_name



@app.route("/files/<path:path>")
def download(path):
    """Download a file."""
    return flask.send_from_directory(app.config['UPLOAD_FOLDER'], path, as_attachment=True)



@app.route('/retrieve', methods=['GET'])
def retrieve_all_files():
	api = ipfsapi.connect('127.0.0.1', 5001)
	mydb,mycursor = db()
	mycursor.execute("SELECT file_name, hash FROM images")
	result_set = mycursor.fetchall()
	for row in result_set:
		file_name = row[0]
		Hash = row[1]
		f=open(app.config['UPLOAD_FOLDER']+file_name,"w+")
		image = api.cat(Hash);
		f.write(image)
		f.close()

	return "Retrived all images onto Pi cluster"


#------------------------Sends the best rated picture --------------------------#
@app.route('/classify', methods=['GET'])
def classify_image():
	classifyUrl = 'https://app.nanonets.com/api/v2/ImageCategorization/LabelFile/'
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	future = asyncio.ensure_future(get_data_asynchronous(classifyUrl,"classification"))
	loop.run_until_complete(future)
	best_image,Hash = extract_best_picture("classification")
	#return flask.send_from_directory(app.config["UPLOAD_FOLDER"],best_image, as_attachment=True)
	return best_image


#------------------------Sends the ones most likely to be cat--------------------------#
@app.route('/detect', methods=['GET'])
def detect_cat():
	detectUrl = 'https://app.nanonets.com/api/v2/ObjectDetection/Model/bf2607e8-d85f-4278-93d3-2efa4038f59b/LabelFile/'
	#loop = asyncio.get_event_loop()
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	future = asyncio.ensure_future(get_data_asynchronous(detectUrl,"detection"))
	loop.run_until_complete(future)
	best_image,Hash = extract_best_picture("detection")
	#return send_from_directory(app.config["UPLOAD_FOLDER"],best_image, as_attachment=True)
	#return flask.send_from_directory(app.config["UPLOAD_FOLDER"],best_image, as_attachment=True)
	return best_image

#================================================= HELPER FUNCITONS FOR PARALLEL CLASSIFICATION =======================================#
START_TIME = default_timer()
def fetch(session, imgPath, url,classif_type):
	print("fetch\n")
	auth = requests.auth.HTTPBasicAuth('TwL75FKFCin_w4Lg4MFplluqsZ6SfESa', '')
	parameters={}
	if classif_type == "detection":
		parameters={'file': open( imgPath, 'rb')}
	elif classif_type == "classification":
		parameters={'file': open( imgPath, 'rb'), 'modelId': ('', '89a6d6cb-bf95-4788-ba7c-911f06c35bc6')}


	with session.post(url, auth=auth, files=parameters) as response:
		data = response.text
		#print(data)
		if response.status_code != 200:
			print("FAILURE::{0}".format(url))
		elapsed = default_timer() - START_TIME
		time_completed_at = "{:5.2f}s".format(elapsed)
		print("{0:<30} {1:>20}".format(imgPath, time_completed_at))
		return data


async def get_data_asynchronous(url,classif_type):
	mydb,mycursor=db()
	imgPath_arr = os.listdir(app.config['UPLOAD_FOLDER'])
	for imgPath in imgPath_arr[:]: # filelist[:] makes a copy of filelist.
	    if not(imgPath.endswith(".png")):
	        imgPath_arr .remove(imgPath)
#print(filelist)


	print(imgPath_arr)
	print("{0:<30} {1:>20}".format("File", "Completed at"))
	with ThreadPoolExecutor(max_workers=10) as executor:
		with requests.Session() as session: # Set any session parameters here before calling `fetch`
			loop = asyncio.get_event_loop()
			START_TIME = default_timer()
			tasks = [
				loop.run_in_executor(
					executor,
					fetch,
					*(session, app.config['UPLOAD_FOLDER']+imgName, url,classif_type)
				)
				for imgName in imgPath_arr
			]

			#-------------  STORE CLASSIFICATION RESULTS INTO LOCAL SQL DB----------------------#
			for response in await asyncio.gather(*tasks):# have the classification results now, do something with the results?
				# Store result into database
				detection_prob = 0
				quality_score = 0
				filename =  ""
				
				
				if classif_type=="detection":
					
					res = ast.literal_eval(response)['result'][0]
					filename = res['input']
					print(res)

					pred = res['prediction'][0]
					detection_prob = pred['score']
				
					

				elif classif_type=="classification":
					#res = ast.literal_eval(response)['result'][0]
					res = ast.literal_eval(response)['result'][0]
					filename = res['file']
					pred = res["prediction"][0]
					print(res)
					#print(pred)
					quality_score = pred["probability"]
					#print(pred)

				#-------------------------Add nice pics to db,  discard bad ones --------------------------#
				if (detection_prob >=0.95 or quality_score >=0.2):   # only pick nice pix
					sql=""
					if (classif_type=="classification"):
						sql = "UPDATE images3 SET classification_score=%s WHERE file_name=%s"
						val = (str(quality_score),filename)
					elif (classif_type=="detection"):
						sql = "UPDATE images3 SET detection_score=%s WHERE file_name=%s"
						val = (str(detection_prob),filename)
					mycursor.execute(sql, val)
					mydb.commit()
				else:
					wipe_file(filename)


#================================= SQL HELPER FUNCTIONS =======================================#

def wipe_file(filename):
	mydb,mycursor = db()
	sql="DELETE FROM images3 WHERE file_name = %s"
	val=(filename)
	mycursor.execute(sql,val)
	mydb.commit()
	file_exists = os.path.isfile('../catpix/%s'%filename)
	if file_exists:
		subprocess.call(["rm","../catpix/"+filename])


def db():
	mydb = mysql.connect( host="localhost",user="root",passwd="Mark1234",db="image_db")
	mycursor = mydb.cursor()
	return mydb,mycursor

def initalize_db():
	mydb,mycursor=db()
	mycursor.execute("CREATE TABLE IF NOT EXISTS %s(file_name VARCHAR(255), hash VARCHAR(255), detection_score FLOAT(24), classification_score FLOAT(24) );")
	val=(app.config['DATABASE_TABLE'])
	mycursor.execute(sql, val)
	mydb.commit()


def extract_best_picture(classification_type):
	mydb,mycursor = db()
	sql=""
	if classification_type=="detection":
		sql="SELECT file_name, hash FROM images3 WHERE detection_score = (SELECT MAX(detection_score) FROM images3)"

	elif classification_type=="classification":
		sql="SELECT file_name, hash FROM images3 WHERE classification_score = (SELECT MAX(classification_score) FROM images3)"
	mycursor.execute(sql)
	result_set = mycursor.fetchall()
	print(result_set)
	filename = str(result_set[0][0])
	Hash = str(result_set[0][1])
	return filename, Hash




#def best_classification():















