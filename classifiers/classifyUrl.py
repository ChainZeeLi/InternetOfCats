#pip install requests
import requests, json
from requests.auth import HTTPBasicAuth



data = {'file': open('testdata_cats/testcat12.jpg', 'rb'), 'modelId': ('', '28343a90-1026-4fd4-835d-01fc684547f0')}


headers = {
    'accept': 'application/x-www-form-urlencoded'
}


url = "https://app.nanonets.com/api/v2/ImageCategorization/LabelUrls/"
r = requests.post(url, auth= requests.auth.HTTPBasicAuth('TwL75FKFCin_w4Lg4MFplluqsZ6SfESa', ''), files=data)
print r.content

