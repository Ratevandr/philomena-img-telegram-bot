import re
from urllib.parse import urlparse
import logging


def isCorrectUrl(msgText):
    if (msgText):
        if (urlInWhiteList(msgText)):
            return True
    return False


def isDeviantart(msgText):
    name = urlparse(msgText).hostname
    if (name == 'www.deviantart.com'):
        return True
    return False

def isFurraffinity(msgText):
    name = urlparse(msgText).hostname
    if (name == 'd.facdn.net'):
        return True
    return False

def getFurraffinityArtist(ImgUrl):
    artPath = urlparse(ImgUrl).path.split('/')
    if (artPath[1] == "art"):
        return artPath[2]
    return ""

def getDeviantartArtist(ImgUrl):
    artPath = urlparse(ImgUrl).path.split('/')
    if (artPath[2] == "art"):
        return artPath[1]
    return ""

# check in whiteList

whiteList = ['www.deviantart.com',
             'd.facdn.net',
             'art.drakony.net',
             'dev-art.drakony.net',
             'userapi.com',  # for vkontakte
             'i.pinimg.com',
             'i.imgur.com']

def urlInWhiteList(imgUrl):
    name = urlparse(imgUrl).hostname

    #check Vk
    if (not name):
        logging.error("Empty url string")
        return False
    hostNameList = name.split('.')
    hostName = ""
    if (len(hostNameList)==3):
        hostName = hostNameList[1] +'.'+ hostNameList[2]
        
    if hostName == 'userapi.com':
        res = re.search("(?P<url>https?://[^\s]+)",  imgUrl)
        r_image = re.search(
                r".*\.(jpg|png|gif|jpeg|webm$)", res.group("url"))
        if (r_image):
            return True
        return False
    if not name in whiteList:
        return False

    if name != "www.deviantart.com":
        return True
    # deviantArt  check
    artPath = urlparse(imgUrl).path.split('/')
    if (len(artPath) < 3 or artPath[2] != "art"):
        return False
    else:
        if (isDeviantart(imgUrl)):
            return True

    res = re.search("(?P<url>https?://[^\s]+)",  imgUrl)
    r_image = re.search(
                r".*\.(jpg|png|gif|jpeg|webm$)", res.group("url"))
    if (r_image):
        return True
    return False

def extractUrlFromString(msgText):
    res = re.search("(?P<url>https?://[^\s]+)", msgText)

    if (res is not None):
        httpUrlStr = res.group("url")
        return httpUrlStr
# imgUrl = isCorrectUrl(
#    """https://i.pinimg.com/originals/1c/e5/db/1ce5dbebdbe6b8cd9dee74a2b6a0ff35.jpg """)

# print(imgUrl)

#print(urlInWhiteList(
 #  "https://cs11.pikabu.ru/post_img/2020/09/29/8/1601382904198781473.jpg"))
# print(isCorrectUrl("https://cs11.pikabu.ru/post_img/2020/09/29/8/"))
# https://d.facdn.net/art/hontoriel/1601189910/1601189910.hontoriel_il_1140xn_2599497791_1azb.jpg
# https://sun9-57.userapi.com/lnd_2r82ADvF4ZiRUCcMYfoYCSf1wlJ7Y-tvgQ/04v2X50JA78.jpg
# https://www.deviantart.com/m4wie/art/Free-like-the-wind-517581621
#print(getDeviantartArtist("https://www.deviantart.com/m4wie/art/Free-like-the-wind-517581621"))
#print(getFurraffinityArtist("https://d.facdn.net/art/hontoriel/1601189910/1601189910.hontoriel_il_1140xn_2599497791_1azb.jpg"))