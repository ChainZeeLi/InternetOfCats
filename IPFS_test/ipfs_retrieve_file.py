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
"""
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
"""




hashs = [
"QmaPuXRfvJBVaiDMCujegunAPLGrUwX6S1NJtCZkGc6rTj",
"QmbMgFLTboy1LjqDMiagjCqMmEReSfnmV4FxBDgmkfcgYR",
"QmUfc85PqJ7vTsHw82xJ7x5oPbFUc6w2kiNzLZv7dqasqi",
"QmcRv9qoN9qe85k4gACZAiRAat2FSV9kewZGgWVnGYqSYQ",
"QmbrBgUTgvA3MPC3MWu6YmgkptPLtQEahnqLjCpvpLd3xm"
]
api = ipfsapi.connect('127.0.0.1', 5001)
file_names = ['1.jpg','2.jpg','3.jpg','4.jpg','5.jpg']
i=0
for h in hashs:
	f= open(file_names[i],"w+")
	image = api.cat(h);
	f.write(image)
	f.close()
	i+=1




