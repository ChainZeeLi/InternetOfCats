import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor
from timeit import default_timer
from os import listdir
from os.path import isfile, join

url = 'https://app.nanonets.com/api/v2/ImageCategorization/LabelFile/'


START_TIME = default_timer()
def fetch(session, imgPath):
    #base_url = "https://people.sc.fsu.edu/~jburkardt/data/csv/"
    #here let's try classifying first     
    #with urlCall(imgPath) as response:
    url = 'https://app.nanonets.com/api/v2/ImageCategorization/LabelFile/'
    parameters = {'file': open(imgPath, 'rb'), 'modelId': ('', '89a6d6cb-bf95-4788-ba7c-911f06c35bc6')}
    #requests.post(url, auth=requests.auth.HTTPBasicAuth('TwL75FKFCin_w4Lg4MFplluqsZ6SfESa', ''), files=data)
    auth = requests.auth.HTTPBasicAuth('TwL75FKFCin_w4Lg4MFplluqsZ6SfESa', '')

    parameters = {'file': open(imgPath, 'rb'), 'modelId': ('', '89a6d6cb-bf95-4788-ba7c-911f06c35bc6')}
    with session.post(url, auth=auth, files=parameters) as response:
        data = response.text
        print(data)
        if response.status_code != 200:
            print("FAILURE::{0}".format(url))

        elapsed = default_timer() - START_TIME
        time_completed_at = "{:5.2f}s".format(elapsed)
        print("{0:<30} {1:>20}".format(imgPath, time_completed_at))
        return data


#async def get_data_asynchronous():
#@asyncio.coroutine 
async def get_data_asynchronous():
    img1 = "/Users/markli/Desktop/InternetOfCats/catpix/cat1.jpg"
    img2 = "/Users/markli/Desktop/InternetOfCats/catpix/cat2.jpg"
    img3 = "/Users/markli/Desktop/InternetOfCats/catpix/cat3.jpg"
    img4 = "/Users/markli/Desktop/InternetOfCats/catpix/cat4.jpg"
    imgPath_arr = [img1,img2,img3,img4]

    print("{0:<30} {1:>20}".format("File", "Completed at"))

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
                    *(session, imgPath)
                )
                for imgPath in imgPath_arr
            ]
            for response in await asyncio.gather(*tasks):
                pass

def main():
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous())
    loop.run_until_complete(future)

main()






