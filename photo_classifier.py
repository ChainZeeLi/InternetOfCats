import requests
from picamera import PiCamera
from time import sleep
from signal import pause
from gpiozero import MotionSensor, LED
from InstagramAPI import InstagramAPI
from PIL import Image
import ast

# This script runs on a Raspberry Pi
pir = MotionSensor(4)
camera = PiCamera()
led = LED(16)

#start the camera
#camera.rotation = 180
#camera.start_preview()

#image image names if taking in a burst
i = 0

#take photo when motion is detected
def take_photo():
    global i
    i = i + 1
    camera.capture('/home/pi/Desktop/bee.jpg')
    image = Image.open('/home/pi/Desktop/bee.jpg')
    image.save('/home/pi/Desktop/' + 'new_bee.jpg')
    url = 'https://app.nanonets.com/api/v2/ImageCategorization/LabelFile/'
    data = {'file': open('/home/pi/Desktop/new_bee.jpg', 'rb'), 'modelId': ('', '28343a90-1026-4fd4-835d-01fc684547f0')}
    response = requests.post(url, auth= requests.auth.HTTPBasicAuth('TwL75FKFCin_w4Lg4MFplluqsZ6SfESa', ''), files=data)
    pred_out = ast.literal_eval(response.text) # convert string to dict
    pred_out=pred_out['result'][0]['prediction']
    pred1 = pred_out[0]
    pred2 = pred_out[1]
    media ='/home/pi/Desktop/new_bee.jpg'
    captionText = 'Hi! this is '+ pred1['label']+ ' with probability ' + str(pred1['probability']) + ' or ' +pred2['label'] + ' with probability ' + str(pred2['probability'])
    ig = InstagramAPI("thisbe_hilbert_autorazzi", "EC544IoC")
    ig.login()
    ig.uploadPhoto(media, caption=captionText)
    print(response.text)
    print('A photo has been taken')
    #sleep(10)
#take_photo()
pir.when_motion =led.on
pir.when_no_motion = led.off
#pir.when_motion=take_photo
pause()

