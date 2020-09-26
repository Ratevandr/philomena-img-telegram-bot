from urllib.request import urlopen
from bs4 import BeautifulSoup

def getImgUrlFromDeviantArt(deviantUrl):
    url = deviantUrl
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")
    
    # kill all script and style elements
    for script in soup(["script", "style", "a"]):
        script.extract()    # rip it out
    
    for link in soup.find_all('img'):
        if (link.get('aria-hidden')):
            return link.get('src')
