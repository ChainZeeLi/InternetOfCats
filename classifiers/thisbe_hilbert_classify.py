import requests

url = 'https://app.nanonets.com/api/v2/ImageCategorization/LabelFile/'

data = {'file': open('REPLACE_IMAGE_PATH.jpg', 'rb'), 'modelId': ('', '28343a90-1026-4fd4-835d-01fc684547f0')}

response = requests.post(url, auth= requests.auth.HTTPBasicAuth('TwL75FKFCin_w4Lg4MFplluqsZ6SfESa', ''), files=data)

print(response.text)