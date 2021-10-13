import requests
import json
import logging

def searchImgPost(fullPathToImg):
    config = ""
    with open('config.json') as config_file:
        config = json.load(config_file)

    fuzzySearchApiKey = config["fuzzy-search-api-key"]
    fuzzyUrl = "https://api.fuzzysearch.net/image?exact"

    header={"x-api-key" : fuzzySearchApiKey}

    with open(fullPathToImg, 'rb') as img:
        files = {'image': (img) }
        with requests.Session() as sess:
            resp = sess.post(fuzzyUrl, files=files,headers=header)
            print(resp.status_code)
            if (resp.status_code == 200):
                    data = resp.text
                    jsonData = json.loads(data)
                    if (len(jsonData["matches"])>0):
                        if (jsonData["matches"][0]["site"]=="FurAffinity"):
                            return "https://www.furaffinity.net/view/"+jsonData["matches"][0]["site_id_str"]
                        else:
                            logging.debug(f"The site isn't furaffinity")
                    else:
                        logging.debug(f"Zero matches")
            else:
                logging.debug(f"FuzzySearch response code is {resp.status_code}")
    return ""
