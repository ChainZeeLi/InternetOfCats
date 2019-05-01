#pip install requests
import requests, json
from requests.auth import HTTPBasicAuth



#data = {'file': open('../testdata_cats/testcat12.jpg', 'rb'), 'modelId': ('', '28343a90-1026-4fd4-835d-01fc684547f0')}
data = {'file': open('../testdata_cats/testcat25.jpg', 'rb')}
headers = {
    'accept': 'application/x-www-form-urlencoded'
}
#url = "https://app.nanonets.com/api/v2/ImageCategorization/LabelUrls/"
url = 'https://app.nanonets.com/api/v2/ObjectDetection/Model/bf2607e8-d85f-4278-93d3-2efa4038f59b/LabelFile/'




url = 'https://app.nanonets.com/api/v2/ImageCategorization/LabelFile/'
data = {'file': open('../catpix/cat3.jpg', 'rb'), 'modelId': ('', '89a6d6cb-bf95-4788-ba7c-911f06c35bc6')}


r = requests.post(url, auth= requests.auth.HTTPBasicAuth('TwL75FKFCin_w4Lg4MFplluqsZ6SfESa', ''), files=data)
print r.content
