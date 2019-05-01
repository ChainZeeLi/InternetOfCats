import requests

url = 'https://app.nanonets.com/api/v2/ObjectDetection/Model/bf2607e8-d85f-4278-93d3-2efa4038f59b/LabelFile/'

data = {'file': open('REPLACE_IMAGE_PATH.jpg', 'rb')}

response = requests.post(url, auth=requests.auth.HTTPBasicAuth('TwL75FKFCin_w4Lg4MFplluqsZ6SfESa', ''), files=data)

print(response.text)