import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import re
import json
import APIdrakony
import db
import tags
import htmlUtil
import os


bot = 0
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Привет! Я ваш новый бот! ')


def dragonOnImageQuestion(update, context):
    fromUserClickedId = update.callback_query.from_user.id
    fromUserSenderId = update.callback_query.message.reply_to_message.from_user.id
    fromUserSenderIName = update.callback_query.message.reply_to_message.from_user.name

    if (fromUserClickedId != fromUserSenderId):
        bot.answer_callback_query(
            callback_query_id=update.callback_query.id, text="Только "+fromUserSenderIName+" может тыкать на кнопки!", show_alert=False)
        return
    msgId = update.callback_query.message.message_id
    groupId = update.callback_query.message.chat.id
    replyMsgText = update.callback_query.message.reply_to_message.text
    imgUrlFromReply = htmlUtil.extractUrlFromString(replyMsgText)
    tagColumnId = db.searchMsgWithImgID(msgId,  groupId)

    query = update.callback_query
    query.answer()
    msgType = query.data
    msgType = msgType.split('_')
    if (len(msgType) < 2):
        return

    if (msgType[0] == 'answ' and msgType[1] == 'false'):
        bot.delete_message(groupId, msgId)
        return

    if (msgType[0] == 'answ'):

        keyboard = [
            [InlineKeyboardButton(
                "eastern dragon", callback_data='tag_eastern')],
            [InlineKeyboardButton(
                "western dragon", callback_data='tag_western')],
            [InlineKeyboardButton("wyvern", callback_data='tag_wyvern')],
            [InlineKeyboardButton("serpent", callback_data='tag_serpent')],
            [InlineKeyboardButton("hydra", callback_data='tag_hydra')],
            [InlineKeyboardButton(
                "amphiptere", callback_data='tag_amphiptere')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("Выберите теги.", reply_markup=reply_markup)
    if (msgType[0] == 'tag'):
        db.insertAnswer(tagColumnId,  msgType[1])
        keyboard = [
            [InlineKeyboardButton("black ⬛️", callback_data='color_black'),
             InlineKeyboardButton("blue 🟦", callback_data='color_blue'),
             InlineKeyboardButton("purple 🟪", callback_data='color_purple'),
             InlineKeyboardButton("bronze 🥉", callback_data='color_bronze')],
            [InlineKeyboardButton("yellow 🟨", callback_data='color_yellow'),
             InlineKeyboardButton("golden 🥇", callback_data='color_golden'),
             InlineKeyboardButton("green 🟢", callback_data='color_green'),
             InlineKeyboardButton("silver 🥈", callback_data='color_silver')],
            [InlineKeyboardButton("grey 🐭", callback_data='color_grey'),
             InlineKeyboardButton("red 🟥", callback_data='color_red'),
             InlineKeyboardButton("white ⬜️", callback_data='color_white'),
             InlineKeyboardButton("rainbow 🌈", callback_data='color_rainbow')],
            [
             InlineKeyboardButton("other ❓", callback_data='color_other'),
             InlineKeyboardButton("SecondColor ➡️🌈", callback_data='color_secondColor'),
             InlineKeyboardButton("Next ➡️", callback_data='color_nextTag')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("Молодец :3 Теперь выбери цвет.", reply_markup=reply_markup)
    
    if (msgType[0]=='color'  and  msgType[1]!='nextTag' and  msgType[1]!='secondColor') :
        db.insertAnswer(tagColumnId,  msgType[1])

    if (msgType[0]=='color'  and  msgType[1]=='secondColor') :
        keyboard = [
            [InlineKeyboardButton("black ⬛️", callback_data='secondColor_scblack'),
             InlineKeyboardButton("blue 🟦", callback_data='secondColor_scblue'),
             InlineKeyboardButton("purple 🟪", callback_data='secondColor_scpurple'),
             InlineKeyboardButton("bronze 🥉", callback_data='secondColor_scbronze')],
            [InlineKeyboardButton("yellow 🟨", callback_data='secondColor_scyellow'),
             InlineKeyboardButton("golden 🥇", callback_data='secondColor_scgolden'),
             InlineKeyboardButton("green 🟢", callback_data='secondColor_scgreen'),
             InlineKeyboardButton("silver 🥈", callback_data='secondColor_scsilver')],
            [InlineKeyboardButton("grey 🐭", callback_data='secondColor_scgrey'),
             InlineKeyboardButton("red 🟥", callback_data='secondColor_scred'),
             InlineKeyboardButton("white ⬜️", callback_data='secondColor_scwhite'),
             InlineKeyboardButton("rainbow 🌈", callback_data='secondColor_scrainbow')],
        [
             InlineKeyboardButton("other ❓", callback_data='secondColor_scother'),
             InlineKeyboardButton("Next ➡️", callback_data='color_nextTag')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            "Выбирай дополнительные цвета.", reply_markup=reply_markup)

    if (msgType[0] == 'secondColor'):
        db.insertAnswer(tagColumnId,  msgType[1])

    if (msgType[0] == 'color' and msgType[1]=='nextTag'):
        
        keyboard = [
            [InlineKeyboardButton("safe ✅", callback_data='rating_safe'),
             InlineKeyboardButton(
                 "suggestive 😏", callback_data='rating_suggestive'),
             InlineKeyboardButton(
                 "questionable ❔", callback_data='rating_questionable'),
             InlineKeyboardButton("explicit 🔞", callback_data='rating_explicit')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            "А ты хорош :3 Теперь выбери рейтинг.", reply_markup=reply_markup)
    if (msgType[0] == 'rating' or msgType[0] == 'moreTags'):
        if (msgType[1] != 'end' and msgType[1] != 'moreTags2' and msgType[1] != 'prev'):
            db.insertAnswer(tagColumnId,  msgType[1])
        keyboard = [
            [InlineKeyboardButton("solo", callback_data='moreTags_solo'),
             InlineKeyboardButton("feath., wings 🦢", callback_data='moreTags_feathWings'),
             InlineKeyboardButton("cave", callback_data='moreTags_cave')],
            [InlineKeyboardButton("spread wings 🦇", callback_data='moreTags_spreadWings'),
             InlineKeyboardButton("breasts", callback_data='moreTags_breasts'),
             InlineKeyboardButton("simple background 👩‍❤️‍💋‍👨", callback_data='moreTags_simpleBackground')],
            [InlineKeyboardButton("mane 🦄", callback_data='moreTags_mane'),
             InlineKeyboardButton("cloud ☁️", callback_data='moreTags_cloud'),
             InlineKeyboardButton("fire 🔥", callback_data='moreTags_fire'),
             InlineKeyboardButton("mlp 🐴", callback_data='moreTags_mlp')],
            [InlineKeyboardButton("forest 🌳", callback_data='moreTags_forest'),
             InlineKeyboardButton("mountain ⛰", callback_data='moreTags_mountain'),
             InlineKeyboardButton("food 🥡", callback_data='moreTags_food')],
            [InlineKeyboardButton("sea", callback_data='moreTags_sea'),
             InlineKeyboardButton("sky 🎈", callback_data='moreTags_sky'),
             InlineKeyboardButton("group ", callback_data='moreTags_group')],
            [InlineKeyboardButton("stars ✨", callback_data='moreTags_stars'),
             InlineKeyboardButton("flying 🕊️", callback_data='moreTags_flying'),
             InlineKeyboardButton("tail fluff 🦨", callback_data='moreTags_tailFluff')],
            [InlineKeyboardButton("fur ", callback_data='moreTags_fur'),
             InlineKeyboardButton("furry", callback_data='moreTags_furry'),
             InlineKeyboardButton("anthro", callback_data='moreTags_anthro')],
            [InlineKeyboardButton("human 🧍", callback_data='moreTags_human'),
             InlineKeyboardButton("male ♂️", callback_data='moreTags_male'),
             InlineKeyboardButton("female ♀️", callback_data='moreTags_female'),
             InlineKeyboardButton("herm ⚥", callback_data='moreTags_herm')],
            [InlineKeyboardButton("MoreTags ➡️", callback_data='moreTags_moreTags2'),
            InlineKeyboardButton("END ✅", callback_data='moreTags_end')]
        ]
        if (msgType[0] != 'moreTags'  and msgType[1]!='end'):
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                "Продолжаем. Вот еще кучка популярных тегов. Что бы закончить жми END ✅", reply_markup=reply_markup)

    # второй выбор
    if (msgType[1] == 'moreTags2' or msgType[0] == 'moreTags2'):
        if (msgType[1] != 'end' and msgType[1] != 'moreTags3' and msgType[1] != 'moreTags2'):
            db.insertAnswer(tagColumnId,  msgType[1])
        keyboard = [
            [InlineKeyboardButton("hair", callback_data='moreTags2_hair'),
             InlineKeyboardButton("photo 📷", callback_data='moreTags2_photo'),
             InlineKeyboardButton("tradi;art", callback_data='moreTags2_tradArt'),
             InlineKeyboardButton("transp; background", callback_data='moreTags2_transparentBackground')],
            [InlineKeyboardButton("animated", callback_data='moreTags2_animated'),
             InlineKeyboardButton("sketch", callback_data='moreTags2_sketch'),
             InlineKeyboardButton("river 🏞️", callback_data='moreTags2_river')],
            [InlineKeyboardButton("city 🌆", callback_data='moreTags2_city'),
             InlineKeyboardButton("nipples", callback_data='moreTags2_nipples'),
             InlineKeyboardButton("monochrome", callback_data='moreTags2_monochrome'),
             InlineKeyboardButton("text", callback_data='moreTags2_text')],
            [InlineKeyboardButton("flower 🌹", callback_data='moreTags2_flower'),
             InlineKeyboardButton("portrait", callback_data='moreTags2_portrait'),
             InlineKeyboardButton("moon 🌙", callback_data='moreTags2_moon')],
            [InlineKeyboardButton("building 🏢", callback_data='moreTags2_building'),
             InlineKeyboardButton("book", callback_data='moreTags2_book'),
             InlineKeyboardButton("weapon", callback_data='moreTags2_weapon')],
            [InlineKeyboardButton("headphones 🎧", callback_data='moreTags2_headphones'),
             InlineKeyboardButton("no wings", callback_data='moreTags2_noWings'),
             InlineKeyboardButton("humanized", callback_data='moreTags2_female')],
            [InlineKeyboardButton("kissing", callback_data='moreTags2_herm'),
             InlineKeyboardButton("hug", callback_data='moreTags2_breasts'),
             InlineKeyboardButton("tree", callback_data='moreTags2_feathWings')],
            [InlineKeyboardButton("clothes 👚", callback_data='moreTags2_humanized'),
             InlineKeyboardButton("grass 🌿", callback_data='moreTags2_furry'),
             InlineKeyboardButton("morning", callback_data='moreTags2_anthro'),
             InlineKeyboardButton("human", callback_data='moreTags2_human')],
            [InlineKeyboardButton("Prev ⬅️", callback_data='rating_prev'),
                InlineKeyboardButton("MoreTags ➡️", callback_data='moreTags_moreTags3'),
            InlineKeyboardButton("END ✅", callback_data='moreTags_end')]
        ]

        if (msgType[0] != 'moreTags2' and msgType[1] =='moreTags2'  ):
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                "Есть еще кучка тегов дальше➡️. Что бы закончить жми END ✅", reply_markup=reply_markup)

    # третий выбор
    if (msgType[1] == 'moreTags3' or msgType[0] == 'moreTags3'):
        if (msgType[1] != 'end' and msgType[1] != 'moreTags3' and msgType[1] != 'moreTags2'):
            db.insertAnswer(tagColumnId,  msgType[1])
        keyboard = [
            [InlineKeyboardButton("morning 🌅", callback_data='moreTags3_morning'),
             InlineKeyboardButton("lying down 🛏️", callback_data='moreTags3_lyingDown'),
             InlineKeyboardButton("lying on nack", callback_data='moreTags3_lyingOnBack'),
             InlineKeyboardButton("evening", callback_data='moreTags3_evening')],
            [InlineKeyboardButton("sun", callback_data='moreTags3_sun'),
             InlineKeyboardButton("moon", callback_data='moreTags3_moon'),
             InlineKeyboardButton("plain", callback_data='moreTags3_plain')],
            [InlineKeyboardButton("coast 🌴", callback_data='moreTags3_coast'),
             InlineKeyboardButton("winter", callback_data='moreTags3_winter'),
             InlineKeyboardButton("summer", callback_data='moreTags3_summer'),
             InlineKeyboardButton("spring", callback_data='moreTags3_spring')],
            [InlineKeyboardButton("fall", callback_data='moreTags3_fall'),
             InlineKeyboardButton("flying", callback_data='moreTags3_flying'),
             InlineKeyboardButton("lies", callback_data='moreTags3_lies')],
            [InlineKeyboardButton("stretching", callback_data='moreTags3_stretching'),
             InlineKeyboardButton("jump", callback_data='moreTags3_jump'),
             InlineKeyboardButton("game", callback_data='moreTags3_game')],
            [InlineKeyboardButton("playing", callback_data='moreTags3_playing'),
             InlineKeyboardButton("cooking", callback_data='moreTags3_cooking'),
             InlineKeyboardButton("space 🌌", callback_data='moreTags3_space')],
            [InlineKeyboardButton("night", callback_data='moreTags3_night'),
             InlineKeyboardButton("dance 💃", callback_data='moreTags3_dance'),
             InlineKeyboardButton("tree", callback_data='moreTags3_tree'),
            InlineKeyboardButton("sitting 🪑", callback_data='moreTags3_sitting')],
            [InlineKeyboardButton("Prev ⬅️", callback_data='moreTags_moreTags2'),
            InlineKeyboardButton("END ✅", callback_data='moreTags_end')]
        ]

        if (msgType[0] != 'moreTags3' and msgType[1] =='moreTags3'  ):
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                "Продолжаем. Вот еще кучка популярных тегов. Что бы закончить жми END ✅", reply_markup=reply_markup)
    # конец выбора
    if (msgType[1] == 'end'):
        tagList = db.getAnswers(tagColumnId)
        APIdrakony.imgSend(imgUrlFromReply, tagList, fromUserSenderIName)
        philomenaUrl=""
        with open('config.json') as config_file:
            config = json.load(config_file)
        if (config):
            philomenaUrl = config["philomena-url"]
        else:
            logging.error("Error read config file")
            return

        keyboard = [[InlineKeyboardButton(
            text="Молодец! А теперь можно перейти в галерею", url=philomenaUrl, callback_data="1")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        deviantArtist=""
        tagsString = ""
        if (htmlUtil.isDeviantart(imgUrlFromReply)):
             deviantArtist = htmlUtil.getDeviantartArtist(imgUrlFromReply)
             tagsString+="#artist_"+deviantArtist+'   '

        if (htmlUtil.isFurraffinity(imgUrlFromReply)):
            furraffinityArtist = htmlUtil.getFurraffinityArtist(imgUrlFromReply)
            tagsString+="#artist_"+furraffinityArtist+'   '

        disablePreview = False
        for val in tagList:
            tag = tags.getFullTageName(val)
            if  not tag:
                continue
            finTag = tag
            finTag = finTag.replace(' ', '_')
            finTag = "#"+finTag.replace(':', '_')
            if (finTag == "#questionable" or finTag == "#explicit"):
                finTag+="🔞"
                disablePreview = True
            if (finTag == "#male"):
                finTag += "♂️"
            if (finTag == "#female"):
                finTag += "♀️"
            if (finTag == "#herm"):
                finTag += "⚥"
            tagsString += finTag+'   '

        replyMsgText += '\n '
        replyMsgText += tagsString
        replyMsgText += "\n Отправлено: "+fromUserSenderIName

        msgId = update.callback_query.message.reply_to_message.message_id
        chatId = update.callback_query.message.chat.id
        bot.delete_message(chatId, msgId)
        bot.delete_message(chatId, update.callback_query.message.message_id)

        # send message 
        if disablePreview==False:
            imgPath = htmlUtil.downloadImage(imgUrlFromReply)
            imgFile = open(imgPath['imgPath'], 'rb')
            if  imgPath['imgExtension']=='gif' or imgPath['imgExtension']=='webm' :
                  bot.send_animation(chatId, imgFile, caption=replyMsgText)
            else:
                bot.send_photo(chatId, imgFile, caption=replyMsgText)
            imgFile.close()
        else:
            bot.send_message(chatId, replyMsgText, reply_markup=reply_markup,  disable_web_page_preview=disablePreview)
        db.deleteOnKind(msgId,  groupId)


def echo(update, context):
    if (not update.message or not update.message.text):
        return
    if (not htmlUtil.isCorrectUrl(str(update.message.text))):
        logging.debug(
            f"Image with url {str(update.message.text)} not supported")
        return

    res = re.search("(?P<url>https?://[^\s]+)", str(update.message.text))

    if (res is not None):
        httpUrlStr = res.group("url")
        imgUrlFromDrakony = APIdrakony.imgSearch(httpUrlStr)

        if imgUrlFromDrakony:
            msgId = update.message.message_id
            chatId = update.message.chat.id
            bot.delete_message(chatId, msgId)
            print(chatId)
            if (imgUrlFromDrakony and (imgUrlFromDrakony['Tags'].find('#explicit') != -1 or imgUrlFromDrakony['Tags'].find('#questionable') != -1)): 
                msgString = imgUrlFromDrakony['Url']+imgUrlFromDrakony['Tags']+'\nRef: '+imgUrlFromDrakony['UrlToPhilomena']
                bot.send_message(chatId, msgString,  disable_web_page_preview=True)
            else:
                bot.send_chat_action(chatId, 'upload_photo')
                imgPath = htmlUtil.downloadImage(imgUrlFromDrakony['Url'])

                imgFile = open(imgPath['imgPath'], 'rb')
                if  imgPath['imgExtension']=='gif' or imgPath['imgExtension']=='webm' :
                      msgCaptionStr = imgUrlFromDrakony['Tags']+'\nRef: '+imgUrlFromDrakony['UrlToPhilomena']
                      bot.send_animation(chatId, imgFile, caption=msgCaptionStr)
                else:
                    msgCaptionStr = imgUrlFromDrakony['Tags']+'\nRef: '+imgUrlFromDrakony['UrlToPhilomena']
                    bot.send_photo(chatId, imgFile, msgCaptionStr)

                imgFile.close()
                if os.path.exists(imgPath['imgPath']):
                    os.remove(imgPath['imgPath'])
                else:
                    logging.error("File "+imgPath['imgPath']+" doesnt exist.")
        else:
 
            keyboard = [[InlineKeyboardButton("Да", callback_data='answ_true'),
                         InlineKeyboardButton("Нет", callback_data='answ_false')]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(
                "На изображении есть дракон?", reply_markup=reply_markup)

def main():
    logging.info("Bot started")
    db.createDB()

    config = ""
    with open('config.json') as config_file:
        config = json.load(config_file)

    token = config["telegram-bot-token"]
    updater = Updater(
        token, use_context=True)
    global bot
    bot = updater.bot
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(dragonOnImageQuestion))

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
