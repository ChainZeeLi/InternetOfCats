import requests
from picamera import PiCamera
from time import sleep
from signal import pause
from gpiozero import MotionSensor, LED
from InstagramAPI import InstagramAPI
from PIL import Image, ImageDraw
import ast

# Initialize peripherals and APIs
pir = MotionSensor(4)
camera = PiCamera()
led = LED(16)
#ig = InstagramAPI("thisbe_hilbert_autorazzi", "ec544ioc")
ig = InstagramAPI("thisbehilbert", "ec544ioc")
#ig.login()
#image image names if taking in a burst
i = 0

#take photo when motion is detected
def take_photo():
    global ig
    #i = i + 1
    led.on()
    camera.capture('/home/pi/Desktop/bee.jpg')
    print('A photo has been taken')
    image = Image.open('/home/pi/Desktop/bee.jpg')
    image.save('/home/pi/Desktop/' + 'new_bee.jpg') #strip EXIF data because it interferes w/instagram API
    # image.show()



#-----------------------------------------------  NEED TO CHANGE THESE, CALL MY SEVERS INSTEAD   -----------------------------------------------------------------------------#
    urlClassify = 'https://app.nanonets.com/api/v2/ImageCategorization/LabelFile/'
    urlDetect = 'https://app.nanonets.com/api/v2/ObjectDetection/Model/bf2607e8-d85f-4278-93d3-2efa4038f59b/LabelFile/'
    dataClassify = {'file': open('/home/pi/Desktop/new_bee.jpg', 'rb'), 'modelId': ('', '28343a90-1026-4fd4-835d-01fc684547$
    dataDetect = {'file': open('/home/pi/Desktop/new_bee.jpg', 'rb')}
    responseDetect = requests.post(urlDetect, auth=requests.auth.HTTPBasicAuth('TwL75FKFCin_w4Lg4MFplluqsZ6SfESa', ''), fil$
    responseClassify = requests.post(urlClassify, auth= requests.auth.HTTPBasicAuth('TwL75FKFCin_w4Lg4MFplluqsZ6SfESa', '')$
    pred_out = ast.literal_eval(responseClassify.text) # convert string to dict
    pred_out=pred_out['result'][0]['prediction']
    pred1 = pred_out[0]
    pred2 = pred_out[1]
    detected = ast.literal_eval(responseDetect.text)
    detected = detected['result'][0]['prediction']
#-----------------------------------------------------------------------------------------------------------------------------------#


    if detected != []:
        print('A cat has been detected')
        media ='/home/pi/Desktop/new_bee.jpg'
        captionText = 'Hi! this is '+ pred1['label']+ ' with probability ' + str(pred1['probability']) + ' or ' +pred2['lab$
        ig.uploadPhoto(media, caption=captionText)
        print(type(ig.LastResponse))
        #response = ig.s.post(self.API_URL + "upload/photo/", data=m.to_string())
        if ig.LastResponse.status_code ==500:
            print("Upload failed, trying again in 10 minutes")
            sleep(600)
            ig.uploadPhoto(media, caption=captionText)
        print(ig.LastResponse)
        print(responseDetect.text)
        sleep(45) # this is to avoid being banned by instagram for bot-like behavior
    led.off()

ig.login()
while 1:
    if pir.motion_detected:
        take_photo()
        #pause()

