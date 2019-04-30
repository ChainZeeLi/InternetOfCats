import requests

url = 'https://app.nanonets.com/api/v2/ImageCategorization/LabelFile/'

data = {'file': open('REPLACE_IMAGE_PATH.jpg', 'rb'), 'modelId': ('', '89a6d6cb-bf95-4788-ba7c-911f06c35bc6')}

response = requests.post(url, auth= requests.auth.HTTPBasicAuth('TwL75FKFCin_w4Lg4MFplluqsZ6SfESa', ''), files=data)

print(response.text)