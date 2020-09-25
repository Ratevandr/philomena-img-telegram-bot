import requests
import logging
import re
import json


def imgSend(imgUrl):
    KEY = "vFqdJFf25ANz0ruZUihJ"
    URL = "https://dev-art.drakony.net/api/v1/json/images?key="+KEY
    print(URL)
    headers = {'Content-type': 'application/json'}
    jsonDict = {
        "image": {
            "description": "",
            "tag_input": "safe, dragon, horse, senshi, one, two",
            "source_url": ""
        },
        "url": imgUrl
    }
    jsonData = json.dumps(jsonDict)

    response = requests.post(url=URL,  data=jsonData, headers=headers)

    data = response.text
    print(data)

    try:
        jsonData = json.loads(data)
    except ValueError as e:
        print("error:"+e)
    
    if "image" not in jsonData:
        print("ERROR")
    return ""

