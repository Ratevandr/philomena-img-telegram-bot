import requests
import json
import tags

def imgSearch(imgUrl):
    URL = "https://dev-art.drakony.net/api/v1/json/search/reverse"

    PARAMS = {'url': imgUrl,
              'distance': 0.25}
    response = requests.post(url=URL, data=PARAMS)

    data = response.text
    # print(data)

    jsonData = json.loads(data)

    print(jsonData)
    if ("total" in jsonData):
        if (jsonData["total"] > 0):
            finalImgUrl = "https://dev-art.drakony.net" + \
                jsonData["images"][0]["representations"]["full"]
            finalImgUrl += "  \n"
            print(finalImgUrl)
            for tag in jsonData["images"][0]["tags"]:
                finTag = tag.replace(' ', '_')
                finTag = finTag.replace(':', '_')
                print(finTag)
                finalImgUrl += " #"+finTag
            return finalImgUrl
        print("Error search")
        return ""
    return ""


def imgSend(imgUrl, tagsList):
    tagsString = ""
    tagsList.append('artist needed')
    tagsList.append('source needed')
    for val in tagsList:
        tagsString += tags.getFullTageName(val)+', '

    tagsString = tagsString[:-2]

    print(tagsString)

    KEY = ""
    URL = "https://dev-art.drakony.net/api/v1/json/images?key="+KEY
    print(URL)
    headers = {'Content-type': 'application/json'}
    jsonDict = {
        "image": {
            "description": "",
            "tag_input": tagsString,
            "source_url": ""
        },
        "url": imgUrl
    }
    print(jsonDict)
    jsonData = json.dumps(jsonDict)

    response = requests.post(url=URL,  data=jsonData, headers=headers)
    data = response.text
 

    try:
        jsonData = json.loads(data)
 
    except ValueError as e:
        print("error:"+e)

    if "image" not in jsonData:
        print("ERROR")
    return ""