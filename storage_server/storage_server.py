from flask import Flask, request
from werkzeug import secure_filename
import os
import ipfsapi
import mysql.connector
import subprocess
import ast


UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = set(['jpg','png'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '.'

urlClassify = 'https://app.nanonets.com/api/v2/ImageCategorization/LabelFile/'
urlDetect = 'https://app.nanonets.com/api/v2/ObjectDetection/Model/bf2607e8-d85f-4278-93d3-2efa4038f59b/LabelFile/'

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

	
	dataClassify = {'file': open('/home/pi/Desktop/new_bee.jpg', 'rb'), 'modelId': ('', '28343a90-1026-4fd4-835d-01fc684547f0')}
	dataDetect = {'file': open('/home/pi/Desktop/new_bee.jpg', 'rb')}

	responseDetect = requests.post(urlDetect, auth=requests.auth.HTTPBasicAuth('TwL75FKFCin_w4Lg4MFplluqsZ6SfESa', ''))
	responseClassify = requests.post(urlClassify, auth= requests.auth.HTTPBasicAuth('TwL75FKFCin_w4Lg4MFplluqsZ6SfESa', ''))
	pred_out = ast.literal_eval(responseClassify.text) # convert string to dict
	pred_out=pred_out['result'][0]['prediction']
	pred1 = pred_out[0]
	pred2 = pred_out[1]
	detected = ast.literal_eval(responseDetect.text)
	detected = detected['result'][0]['prediction']
   #if detected != []:
	return ""







url = 'https://app.nanonets.com/api/v2/ImageCategorization/LabelFile/'


START_TIME = default_timer()
def fetch(session, imgPath):
    #base_url = "https://people.sc.fsu.edu/~jburkardt/data/csv/"
    #here let's try classifying first     
    #with urlCall(imgPath) as response:
    url = 'https://app.nanonets.com/api/v2/ImageCategorization/LabelFile/'
    parameters = {'file': open(imgPath, 'rb'), 'modelId': ('', '89a6d6cb-bf95-4788-ba7c-911f06c35bc6')}
    #requests.post(url, auth=requests.auth.HTTPBasicAuth('TwL75FKFCin_w4Lg4MFplluqsZ6SfESa', ''), files=data)
    auth = requests.auth.HTTPBasicAuth('TwL75FKFCin_w4Lg4MFplluqsZ6SfESa', '')

    parameters = {'file': open(imgPath, 'rb'), 'modelId': ('', '89a6d6cb-bf95-4788-ba7c-911f06c35bc6')}
    with session.post(url, auth=auth, files=parameters) as response:
        data = response.text
        print(data)
        if response.status_code != 200:
            print("FAILURE::{0}".format(url))

        elapsed = default_timer() - START_TIME
        time_completed_at = "{:5.2f}s".format(elapsed)
        print("{0:<30} {1:>20}".format(imgPath, time_completed_at))
        return data


#async def get_data_asynchronous():
#@asyncio.coroutine 
async def get_data_asynchronous():
    img1 = "/Users/markli/Desktop/InternetOfCats/catpix/cat1.jpg"
    img2 = "/Users/markli/Desktop/InternetOfCats/catpix/cat2.jpg"
    img3 = "/Users/markli/Desktop/InternetOfCats/catpix/cat3.jpg"
    img4 = "/Users/markli/Desktop/InternetOfCats/catpix/cat4.jpg"
    imgPath_arr = [img1,img2,img3,img4]

    print("{0:<30} {1:>20}".format("File", "Completed at"))

    with ThreadPoolExecutor(max_workers=10) as executor:
        with requests.Session() as session:
            # Set any session parameters here before calling `fetch`
            loop = asyncio.get_event_loop()
            START_TIME = default_timer()
            tasks = [
                loop.run_in_executor(
                    executor,
                    fetch,
                    *(session, imgPath)
                )
                for imgPath in imgPath_arr
            ]
            for response in await asyncio.gather(*tasks):
            	# have the classification results now, do something with the results?
                pass

def main():
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous())
    loop.run_until_complete(future)

main()






