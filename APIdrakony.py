import requests
import json
import tags
import logging
import deviantart
import htmlUtil


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
        'Url': '',
        'Tags': ''
    }

    if ("total" in jsonData):
        if (jsonData["total"] > 0):
            urlToPhilomena = philomenaUrl+"/images/" + \
                str(jsonData["images"][0]["id"])
            finalImgUrl['UrlToPhilomena'] = urlToPhilomena
            finalImgUrl['Url'] = philomenaUrl + \
                jsonData["images"][0]["representations"]["full"]
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
                finalImgUrl['Tags'] += " #"+finTag
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
    tagsString = ""
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
                sourceImgUrl = "https://www.furaffinity.net/user/" + \
                    str(furraffinityArtist)+"/"
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
            "description": "Sent by "+author+" from telegram bot",
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

    logging.debug(f"Sended JSON {jsonDict}")

    if "image" not in jsonData:
        err = "Unknown Error: "+json.dumps(jsonData)
        logging.error(
            f"Error while sending image: - image key not found in JSON {jsonData}")
        logging.error(f"Sended JSON {jsonDict}")
        if "errors" in jsonData and "tag_input" in jsonData["errors"]:
            err =  jsonData["errors"]["tag_input"][0]
            if err =="must contain at least one rating tag":
                err = "Пропущен тег рейтинга!"
            return err
        if "errors" in jsonData and "image" in jsonData["errors"]:
            err = jsonData["errors"]["image"][0]
            if err == "can't be blank":
                err = "Не удалось загрузить изображение :("
            return err
        return err
    logging.info(f"Successful send img with url {realImgUrl}")
    return 


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
