from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

tags1 = {
"eastern dragon":'tag_eastern',
"western dragon":'tag_western',
"wyvern":'tag_wyvern',
"serpent":'tag_serpent',
"hydra":'tag_hydra',
 "amphiptere":'tag_amphiptere',
 "Next ➡️":"service_next"
 }

tags2 = {
"safe ✅":"rating_safe",
"suggestive 😏":"rating_suggestive",
 "questionable ❔":"rating_questionable",
 "explicit 🔞":"rating_explicit",
 "Prev ⬅️":"service_prev",
"Next ➡️":"service_next",
"END ✅":'service_end'
 }

tags3 = {
"black ⬛️":"color_black",
"blue 🟦":"color_blue",
"purple 🟪":"color_purple",
"bronze 🥉":"color_bronze",
"yellow 🟨":"color_yellow",
"golden 🥇":"color_golden",
"green 🟢":"color_green",
"silver 🥈":"color_silver",
"grey 🐭":"color_grey",
"red 🟥":"color_red",
"white ⬜️":"color_white",
"rainbow 🌈":"color_rainbow",
"other ❓":"color_other",
"Prev ⬅️":"service_prev",
"Next ➡️":"service_next",
"END ✅":'service_end'
 }

tags4 = {
"black ⬛️":"secondColor_scblack",
"blue 🟦" :"secondColor_scblue",
"purple 🟪":"secondColor_scpurple",
"bronze 🥉":"secondColor_scbronze",
"yellow 🟨":"secondColor_scyellow",
"golden 🥇":"secondColor_scgolden",
"green 🟢":"secondColor_scgreen",
"silver 🥈":"secondColor_scsilver",
"grey 🐭":"secondColor_scgrey",
"red 🟥":"secondColor_scred",
"white ⬜️":"secondColor_scwhite",
"rainbow 🌈":"secondColor_scrainbow",
"other ❓":"secondColor_scother",
"Prev ⬅️":"service_prev",
"Next ➡️":"service_next",
"END ✅":'service_end'
 }


tags5 = {
"gryphon":'tag_gryphon',
"bird 🐦":'tag_bird',
"snake 🐍":'tag_snake',
"human 🧍":'tag_human',
"furry":'tag_furry',
"lizzard 🦎":'tag_lizzard',
"hippogriff":'tag_hippogriff',
"unicorn 🦄":'tag_unicorn',
"horse 🐴":'tag_horse',
"pegas":'tag_pegas',
"mlp 🐴":'tag_mlp',
"anthro":'tag_anthro',
"humanized":'tag_humanized',
"feline 🐈":'tag_feline',
'canine 🐺':'tag_canine',
"Prev ⬅️":"service_prev",
 "Next ➡️":"service_next",
 "END ✅":'service_end'
 }
 
tags6 = {"solo":'moreTags_solo',
"feath., wings 🦢":'moreTags_feathWings',
"cave":'moreTags_cave',
"spread wings 🦇":'moreTags_spreadWings',
"breasts":'moreTags_breasts',
"simple background 👩‍❤️‍💋‍👨":'moreTags_simpleBackground',
"mane 🦄":'moreTags_mane',
"cloud ☁️":'moreTags_cloud',
"fire 🔥":'moreTags_fire',
"rain 🌧":'moreTags_rain',
"forest 🌳":'moreTags_forest',
"mountain ⛰":'moreTags_mountain',
"food 🥡":'moreTags_food',
"sea":'moreTags_sea',
"sky 🎈":'moreTags_sky',
"group ":'moreTags_group',
"stars ✨":'moreTags_stars',
"flying 🕊️":'moreTags_flying',
"tail fluff 🦨":'moreTags_tailFluff',
"fur ":'moreTags_fur',
"male ♂️":'moreTags_male',
"female ♀️":'moreTags_female',
"herm ⚥":'moreTags_herm',
"Prev ⬅️":"service_prev",
"MoreTags ➡️":"service_next",
"END ✅":'service_end'}
 
tags7 = {"hair":'moreTags2_hair',
"photo 📷":'moreTags2_photo',
"tradi;art":'moreTags2_tradArt',
"transp; background":'moreTags2_transparentBackground',
"animated":'moreTags2_animated',
"sketch":'moreTags2_sketch',
"river 🏞️":'moreTags2_river',
"city 🌆":'moreTags2_city',
"nipples":'moreTags2_nipples',
"monochrome":'moreTags2_monochrome',
"text":'moreTags2_text',
"flower 🌹":'moreTags2_flower',
"portrait":'moreTags2_portrait',
"moon 🌙":'moreTags2_moon',
"building 🏢":'moreTags2_building',
"book📖":'moreTags2_book',
"weapon":'moreTags2_weapon',
"headphones 🎧":'moreTags2_headphones',
"no wings":'moreTags2_noWings',
"kissing💏":'moreTags2_kissing',
"hug":'moreTags2_hug',
"tree":'moreTags2_tree',
"clothes 👚":'moreTags2_clothes',
"grass 🌿":'moreTags2_grass',
"morning":'moreTags2_morning',
"Prev ⬅️":'service_prev',
"MoreTags ➡️":'service_next',
"END ✅":'service_end'}
 
tags8 = {"morning 🌅":'moreTags3_morning',
"lying down 🛏️":'moreTags3_lyingDown',
"lying on nack":'moreTags3_lyingOnBack',
"evening":'moreTags3_evening',
"sun":'moreTags3_sun',
"plain":'moreTags3_plain',
"coast 🌴":'moreTags3_coast',
"winter":'moreTags3_winter',
"summer":'moreTags3_summer',
"spring":'moreTags3_spring',
"fall":'moreTags3_fall',
"flying":'moreTags3_flying',
"treasure💰":'moreTags3_treasure',
"stretching":'moreTags3_stretching',
"jump":'moreTags3_jump',
"game":'moreTags3_game',
"playing":'moreTags3_playing',
"cooking":'moreTags3_cooking',
"space 🌌":'moreTags3_space',
"night":'moreTags3_night',
"dance 💃":'moreTags3_dance',
"tree":'moreTags3_tree',
"sitting 🪑":'moreTags3_sitting',
"Prev ⬅️":'service_prev',
"END ✅":'service_end'}
 

 
def updateKeyboard(num, buttonInLine):

    if num == 1:
        return tagToKeyboard(tags1, buttonInLine, num)
    elif num == 2:
        return tagToKeyboard(tags2, buttonInLine, num)
    elif num == 3:
        return tagToKeyboard(tags3, buttonInLine, num)
    elif num == 4:
        return tagToKeyboard(tags4, buttonInLine, num)
    elif num == 5:
        return tagToKeyboard(tags5, buttonInLine, num)
    elif num == 6:
        return tagToKeyboard(tags6, buttonInLine, num)
    elif num == 7:
        return tagToKeyboard(tags7, buttonInLine, num)
    elif num == 8:
        return tagToKeyboard(tags8, buttonInLine, num)


def tagToKeyboard(tags, buttonInLine, num):
    keyboard = []
    buttonCounter = 0
    buttonArray = []
 

    for key in tags:
        if buttonCounter==buttonInLine:
            keyboard.append(buttonArray.copy())
            buttonArray.clear()
            buttonCounter = 0
        callbackDataDict = {
            "tagsListNumber":num,
            "tag":tags[key]
        }
        buttonArray.append(InlineKeyboardButton(key, callback_data=str(callbackDataDict)))
        buttonCounter+=1

    if (len(buttonArray)>0):
        keyboard.append(buttonArray.copy())

    return keyboard
 