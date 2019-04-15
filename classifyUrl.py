

#pip install requests
import requests, json
from requests.auth import HTTPBasicAuth
data = {
    "urls": ["https://s3-us-west-2.amazonaws.com/nanonets/replace_me.jpg"], \
    "modelId":"28343a90-1026-4fd4-835d-01fc684547f0"
}

headers = {
    'accept': 'application/x-www-form-urlencoded'
}


url = "https://app.nanonets.com/api/v2/ImageCategorization/LabelUrls/"
r = requests.post(url, headers=headers, data=data, auth=HTTPBasicAuth('TwL75FKFCin_w4Lg4MFplluqsZ6SfESa', ''))
print r.content

