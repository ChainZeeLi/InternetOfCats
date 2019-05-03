import requests
import shutil
import ast
r = requests.get("http://127.0.0.1:5000/detect")

"""
with open('cat1.jpg', 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)    
"""

res = ast.literal_eval(r)['result'][0]
print res