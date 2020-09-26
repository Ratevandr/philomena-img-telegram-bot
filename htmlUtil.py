import re
from urllib.parse import urlparse


def isCorrectUrl(msgText):
    res = re.search("(?P<url>https?://[^\s]+)",  msgText)
    r_image = ""
    if (isDeviantUrl(msgText)):
        return True
    else:
        r_image = re.search(r".*\.(jpg|png|gif|jpeg|webm$)", res.group("url"))

    httpUrlStr = ""
    if (res is not None) and (r_image is not None):
        httpUrlStr = res.group("url")

    if (httpUrlStr):
        return True
    return False


def isDeviantUrl(imgUrl):
    urlparse(imgUrl)
    name = urlparse(imgUrl).hostname
    if (name == "www.deviantart.com"):
        return True
    return False


imgUrl = isCorrectUrl(
    """https://www.deviantart.com/wifous/art/Reeeee-Sketch-856275439 """)

# print(imgUrl)

# isDeviantUrl("https://www.deviantart.com/moonandqibli/art/AT-Sekicion-856240142")
