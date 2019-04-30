import ipfsapi
import mysql.connector
import requests, json
from requests.auth import HTTPBasicAuth
# needs to install mysql on raspberry pi first

# for db connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Mark1234",
  db="image_db"
)	

while True:
	mycursor.execute("SELECT file_name, hash FROM images")
	myresult = mycursor.fetchall()
	# retrieve each image from IPFS with hash

	for Name, Hash in myresult:
		f= open(file_name,"w+")
		image = api.cat(Hash);
		f.write(image)
		f.close()
		
		data = {'file': open(Name, 'rb'), 'modelId': ('', '28343a90-1026-4fd4-835d-01fc684547f0'). }
		headers = {'accept': 'application/x-www-form-urlencoded'}

		url = "https://app.nanonets.com/api/v2/ImageCategorization/LabelUrls/"
		response = requests.post(url, auth= requests.auth.HTTPBasicAuth('TwL75FKFCin_w4Lg4MFplluqsZ6SfESa', ''), files=data)

		print(response.text)

    	mycursor.execute("DELETE FROM img WHERE hash=%s"%Hash)
    	subprocess.call(["rm", Name])








