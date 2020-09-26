import re

def getImgUrlFromMsg(msgText):
    res = re.search("(?P<url>https?://[^\s]+)",  msgText)
    print("tyc: "+str(res))
    r_image = re.search(r".*\.(jpg|png|gif|jpeg|webm)$", res.group("url"))

    if (res is not None) and (r_image is not None):
        httpUrlStr = res.group("url")
    return httpUrlStr


imgUrl = getImgUrlFromMsg("""https://art.drakony.net/img/view/2020/9/12/11.png  lolkekchecsdfgdfgdfg\
    dfgdfgdfgdfgdfgdfg
    sdfsdf
    https://art.drakony.net/kek.png """)

print(imgUrl)