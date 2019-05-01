import requests
import shutil
r = requests.get("http://127.0.0.1:5000/files/cat88.jpg")
with open('cat1.jpg', 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)    