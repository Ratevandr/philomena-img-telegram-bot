tagsDit = {
    "eastern": "eastern dragon",
    "western": "western dragon",
    "wyvern": "wyvern",
    "serpent": "serpent",
    "hydra": "hydra",
    "amphiptere": "amphiptere",
    "black": "color:black",
    "blue": "color:blue",
    "bronze": "color:bronze",
    "golden": "color:golden",
    "green": "color:green",
    "silver": "color:silver",
    "grey": "color:grey",
    "red": "color:red",
    "white": "color:white",
    "yellow": "color:yellow",
    "rainbow": "color:rainbow",
    "purple": "color:purple",
    "other": "color:other",
    "scblack": "multicolor:black",
    "scblue": "multicolor:blue",
    "scbronze": "multiсolor:bronze",
    "scgolden": "multicolor:golden",
    "scgreen": "multicolor:green",
    "scsilver": "multicolor:silver",
    "scgrey": "multicolor:grey",
    "scred": "multicolor:red",
    "scwhite": "multicolor:white",
    "scyellow": "multicolor:yellow",
    "scrainbow": "multicolor:rainbow",
    "scpurple": "multicolor:purple",
    "scother": "multicolor:other",
    "safe": "safe",
    "suggestive": "suggestive",
    "questionable": "questionable",
    "explicit": "explicit",
    "solo": "solo",  # more tags
    "feathWings": "feathered wings",
    "cave": "cave",
    "spreadWings": "spread wings",
    "breasts": "breasts",
    "simpleBackground": "simple background",
    "mane": "mane",
    "cloud": "cloud",
    "fire": "fire",
    "forest": "forest",
    "mountain": "mountain",
    "food": "food",
    "sea": "sea",
    "sky": "sky",
    "group": "group",
    "stars": "stars",
    "flying": "flying",
    "tailFluff": "tail fluff",
    "fur": "fur",
    "furry": "furry",
    "anthro": "anthro",
    "human": "human",
    "male": "male",
    "female": "female",
    "herm": "herm",
    "mlp": "mlp",
    "hair": "hair",  # moreTags2
    "photo": "photo",
    "transparentBackground": "transparent background", 
    "tradArt": "traditional art",
    "animated": "animated",
    "sketch": "sketch",
    "river": "river",
    "city": "city",
    "nipples": "nipples",
    "monochrome": "monochrome",
    "text": "text",
    "flower": "flower",
    "portrait": "portrait",
    "moon": "moon",
    "building": "building",
    "book": "book",
    "weapon": "weapon",
    "headphones": "headphones",
    "noWings": "no wings",
    "humanized": "humanized",
    "kissing": "kissing",
    "hug": "hug",
    "tree": "tree",
    "clothes": "clothes",
    "grass": "grass",
    "morning": "morning",  # moreTags3
    "lyingDown": "lying down",
    "lyingOnBack": "lying on back",
    "evening": "evening",
    "sun": "sun",
    "moon": "moon",
    "plain": "plain",
    "coast": "coast",  # побережье
    "winter": "winter",
    "summer": "summer",
    "spring": "spring",
    "fall": "fall",
    "flying": "flying",
    "lies": "lies",
    "stretching": "stretching",  # потягушки
    "jump": "jump",
    "game": "game",
    "playing": "playing",
    "cooking": "cooking",
    "space": "space",
    "night": "night",
    "dance": "dance",
    "sitting":"sitting",
    "artist needed": "artist needed",  #additional tags
    "source needed": "source needed",
    "artist questionable": "artist questionable",
    "useless source url": "useless source url"}


def getFullTageName(tagName):
    if tagName in tagsDit:
        return tagsDit[tagName]
    else:
        print("Error "+tagName+" not found!")
        return ""
    
