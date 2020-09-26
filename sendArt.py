import requests
import logging
import re
import json
import deviantart


def imgSend(imgUrl):
    KEY = "vFqdJFf25ANz0ruZUihJ"
    URL = "https://dev-art.drakony.net/api/v1/json/images?key="+KEY
    print(URL)
    realImgUrl = deviantart.getImgUrlFromDeviantArt(imgUrl)
    print(realImgUrl)
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
        logging.error(f"Error while sending img. Json parse error:  {e}")
    
    if "image" not in jsonData:
        logging.error(f"Error while sending img:  {e}")
    return ""

