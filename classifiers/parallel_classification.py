import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor
from timeit import default_timer
from os import listdir
from os.path import isfile, join
import ast
#import mysql.connector
import pymysql as mysql



START_TIME = default_timer()
def fetch(session, imgPath):
    #base_url = "https://people.sc.fsu.edu/~jburkardt/data/csv/"
    #here let's try classifying first     
    #with urlCall(imgPath) as response:
    url =  "https://app.nanonets.com/api/v2/ObjectDetection/Model/bf2607e8-d85f-4278-93d3-2efa4038f59b/LabelFile/"
    url = 'https://app.nanonets.com/api/v2/ImageCategorization/LabelFile/'
    url = 'https://app.nanonets.com/api/v2/ImageCategorization/LabelFile/'
    parameters =  {'file': open(imgPath, 'rb')}
    parameters =  dataClassify = {'file': open(imgPath, 'rb'), 'modelId': ('', '28343a90-1026-4fd4-835d-01fc684547f0')}
    parameters =  dataClassify = {'file': open(imgPath, 'rb'), 'modelId': ('', '89a6d6cb-bf95-4788-ba7c-911f06c35bc6')}


    #requests.post(url, auth=requests.auth.HTTPBasicAuth('TwL75FKFCin_w4Lg4MFplluqsZ6SfESa', ''), files=data)
    auth = requests.auth.HTTPBasicAuth('TwL75FKFCin_w4Lg4MFplluqsZ6SfESa', '')

    #parameters = {'file': open(imgPath, 'rb'), 'modelId': ('', '89a6d6cb-bf95-4788-ba7c-911f06c35bc6')}

    with session.post(url, auth=auth, files=parameters) as response:
        data = response.text
     #   print(data)
        if response.status_code != 200:
            print("FAILURE::{0}".format(url))

        elapsed = default_timer() - START_TIME
        time_completed_at = "{:5.2f}s".format(elapsed)
        print("{0:<30} {1:>20}".format(imgPath, time_completed_at))
        return data


#async def get_data_asynchronous():
#@asyncio.coroutine 
async def get_data_asynchronous():
    mydb = mysql.connect( host="localhost",user="root",passwd="Mark1234",db="image_db")
    mycursor = mydb.cursor()
    

    img1 = "/Users/markli/Desktop/InternetOfCats/catpix/cat1.jpg"
    img2 = "/Users/markli/Desktop/InternetOfCats/catpix/cat2.jpg"
    img3 = "/Users/markli/Desktop/InternetOfCats/catpix/cat3.jpg"
    img4 = "/Users/markli/Desktop/InternetOfCats/catpix/cat4.jpg"

    imgPath_arr = [img1,img2,img3,img4]

    print("{0:<30} {1:>20}".format("File", "Completed at"))
    imgPath_arr = listdir("../catpix")
    with ThreadPoolExecutor(max_workers=10) as executor:
        with requests.Session() as session:
            # Set any session parameters here before calling `fetch`
            loop = asyncio.get_event_loop()
            START_TIME = default_timer()
            tasks = [
                loop.run_in_executor(
                    executor,
                    fetch,
                #    *(session, csv) # Allows us to pass in multiple arguments to `fetch`
                    *(session, "../catpix/"+imgPath)
                )
                for imgPath in imgPath_arr
            ]
            for response in await asyncio.gather(*tasks):
                # Store result into database
                res = ast.literal_eval(response)['result'][0]
                print(res)
                pred = res['prediction']
                #score = pred ['score']
               # print(score)
               # probability = pred['probability']
               # print(probability )

               # filename =  res['file']
               # sql = "UPDATE images3 SET detection_score=%s WHERE file_name=%s"
              #  val = (str(probability),filename)
                #mycursor.execute(sql, val)
                #mydb.commit()


def main():
    loop = asyncio.get_event_loop()
    print(loop)
    future = asyncio.ensure_future(get_data_asynchronous())
    loop.run_until_complete(future)

main()






