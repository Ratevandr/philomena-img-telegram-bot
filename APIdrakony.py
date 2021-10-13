import requests
import json
import tags
import logging
import deviantart
import htmlUtil
import fuzzySearch
from urllib.parse import urlparse
from os.path import splitext, basename

allowMediaFormat = [".jpg",".jpeg",".png",".bmp",".gif",".webm",".mp4",".avi",".swf",".svg"]

def checkSourceUrlPost(sourceUrl):
    curPath = urlparse(sourceUrl)
    filename, fileExt = splitext(basename(curPath.path))
    print(fileExt)
    if fileExt in allowMediaFormat:
        return False
    return True

def imgSearch(imgUrl):
    if (htmlUtil.isDeviantart(imgUrl)):
        imgUrl = deviantart.getImgUrlFromDeviantArt(imgUrl)
    config = ""
    with open('config.json') as config_file:
        config = json.load(config_file)

    philomenaUrl = config["philomena-url"]
    URL = philomenaUrl+"/api/v1/json/search/reverse"

    PARAMS = {'url': imgUrl,
              'distance': 0.25}
    response = requests.post(url=URL, data=PARAMS)

    data = response.text
    jsonData = json.loads(data)

    finalImgUrl = {
        "philomenaPostUrl":None,
        "sourcePostUrl":None,
        "philomenaImgUrl":None,
        'Tags': ''
    }
            

    if ("total" in jsonData):
        if (jsonData["total"] > 0):
            philomenaPostUrl = philomenaUrl+"/images/" + \
                str(jsonData["images"][0]["id"])
            finalImgUrl['philomenaPostUrl'] = philomenaPostUrl
            finalImgUrl['philomenaImgUrl'] = philomenaUrl + \
                jsonData["images"][0]["representations"]["full"]
            sourcePostUrl = jsonData["images"][0]["source_url"]
            if (checkSourceUrlPost(sourcePostUrl)):
                finalImgUrl['sourcePostUrl'] = sourcePostUrl
            for tag in jsonData["images"][0]["tags"]:
                finTag = tag.replace(' ', '_')
                finTag = finTag.replace(':', '_')
                if (finTag == "questionable" or finTag == "explicit"):
                    finTag += "🔞"
                if (finTag == "male"):
                    finTag += "♂️"
                if (finTag == "female"):
                    finTag += "♀️"
                if (finTag == "herm"):
                    finTag += "⚥"
                finalImgUrl['Tags'] += "#"+finTag+" "
            if jsonData["images"] and jsonData["images"][0] and jsonData["images"][0]["description"]:
                desc = jsonData["images"][0]["description"]
                desc = desc.replace('@', ' ')
                finalImgUrl['Tags'] += " \n"+desc
            return finalImgUrl
        return ""
    return ""


def imgSend(imgUrl, tagsList, author):
    config = ""
    with open('config.json') as config_file:
        config = json.load(config_file)

    philomenaUrl = config["philomena-url"]
    philomenaKey = config["philomena-key"]

    URL = philomenaUrl+"/api/v1/json/images?key="+philomenaKey
    realImgUrl = ""
    sourceImgUrl = ""
    artistImgUrl = ""
    tagsString = ""
    postUrlGet = False
    if (htmlUtil.isDeviantart(imgUrl)):
        realImgUrl = deviantart.getImgUrlFromDeviantArt(imgUrl)
        deviantArtist = htmlUtil.getDeviantartArtist(imgUrl)
        if (deviantArtist):
            tagsString += 'artist:'+str(deviantArtist)+', '
            sourceImgUrl = imgUrl
    else:
        if (htmlUtil.isFurraffinity(imgUrl)):
            furraffinityArtist = htmlUtil.getFurraffinityArtist(imgUrl)
            if (furraffinityArtist):
                tagsString += 'artist:'+str(furraffinityArtist)+', '
                tagsList.append('useless source url')
                realImgUrl = imgUrl
                artistImgUrl = "https://www.furaffinity.net/user/" + \
                    str(furraffinityArtist)+"/"
                
                 
                imgPath = htmlUtil.downloadImage(imgUrl)
                sourceImgUrl = fuzzySearch.searchImgPost(imgPath["imgPath"])
                postUrlGet = True
            else:
                logging.error("Error getting furraffinity artist!")
        else:
            realImgUrl = imgUrl
            tagsList.append('artist needed')
            tagsList.append('source needed')

    for val in tagsList:
        tag =  tags.getFullTageName(val)
        if  not tag:
            continue
        tagsString +=tag+', '

    tagsString = tagsString[:-2]

    headers = {'Content-type': 'application/json'}
    jsonDict = {
        "image": {
            "description": f"Sent by {author} from telegram bot \nartist url: {artistImgUrl}",
            "tag_input": tagsString,
            "source_url": sourceImgUrl
        },
        "url": realImgUrl
    }

    jsonData = json.dumps(jsonDict)

    response = requests.post(url=URL,  data=jsonData, headers=headers)
    data = response.text

    try:
        jsonData = json.loads(data)

    except ValueError as e:
        logging.error(f"Error while sending image: {e}")
        return e

    res = {
        "error":None,
        "philomenaPostUrl":None,
        "sourcePostUrl":None,
        "philomenaImgUrl":None
    }

    if "image" not in jsonData:
        res["error"] = "Unknown Error: "+json.dumps(jsonData)
        logging.error(
            f"Error while sending image: - image key not found in JSON {jsonData}")
        logging.error(f"Sended JSON {jsonDict}")
        if "errors" in jsonData and "tag_input" in jsonData["errors"]:
            res["error"] =  jsonData["errors"]["tag_input"][0]
            if res["error"] =="must contain at least one rating tag":
                res["error"] = "Пропущен тег рейтинга!"
            return res
        if "errors" in jsonData and "image" in jsonData["errors"]:
            res["error"] = jsonData["errors"]["image"][0]
            if res["error"] == "can't be blank":
                res["error"] = "Не удалось загрузить изображение :("
            return res
        return res
    logging.info(f"Successful send img with url {realImgUrl}")
    philomenaImgId = jsonData["image"]["id"]
    philomenaFullImgUrl =  jsonData["image"]["representations"]["full"]
    sourcePostUrl = None
    if postUrlGet:
        sourcePostUrl = sourceImgUrl
   
    res["philomenaPostUrl"] = f"{philomenaUrl}/images/{philomenaImgId}"
    res["sourcePostUrl"] = sourcePostUrl
    res["philomenaImgUrl"] = f"{philomenaUrl}/{philomenaFullImgUrl}"
 
    return res


def tagPopularity():
    with open('config.json') as config_file:
        config = json.load(config_file)

    philomenaUrl = config["philomena-url"]
    philomenaUrl = "https://art.drakony.net"

    tagsArray = {}

    for imageId in range(1, 3349):
        print("Process "+str(imageId))

        URL = philomenaUrl+"/api/v1/json/images/"+str(imageId)
        response = requests.get(url=URL)
        data = response.text
        jsonData = json.loads(data)

        if ("image" in jsonData):
            if ("tags" in jsonData["image"]):
                for key in jsonData["image"]["tags"]:

                    if (key in tagsArray):
                        tagsArray[key] = tagsArray[key]+1
                    else:
                        tagsArray[key] = 1

    tagsArraySorted = dict(sorted(tagsArray.items(), key=lambda item: item[1], reverse=True))

    tagFile = open("tag.csv", "w")
    for key in tagsArraySorted:
        print(key+" "+str(tagsArraySorted[key]))
        tagFile.write(key+","+str(tagsArraySorted[key])+'\n')
    tagFile.close()
