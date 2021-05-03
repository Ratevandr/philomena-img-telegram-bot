import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import tagKeyboard
import re
import json
import APIdrakony
import db
import tags
import htmlUtil
import os



bot = 0
artGalleryUrl = ""
arrayNSFWchat = []
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def chatIsNSFW(disablePreview,  chatId):
    if disablePreview == True:
        for nsfwChatId in arrayNSFWchat:
            if str(nsfwChatId) == str(chatId):
                return True
    return False

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Привет! Я ваш новый бот! ')

def dragonOnImageQuestionWithException(update, context):
    try:
        dragonOnImageQuestion(update, context)
    except Exception as err:
        logging.exception("Error: {0}".format(err))
        msgId = update.callback_query.message.reply_to_message.message_id
        chatId = update.callback_query.message.chat.id
        replyMsgText = update.callback_query.message.reply_to_message.text
        imgUrlFromReply = htmlUtil.extractUrlFromString(replyMsgText)
        fromUserSenderIName = update.callback_query.message.reply_to_message.from_user.name
        db.deleteOnKind(msgId,  chatId)

        bot.delete_message(chatId, msgId)
        bot.delete_message(chatId, update.callback_query.message.message_id)
        bot.send_message(chatId, fromUserSenderIName+" сорян соряныч. Произошла ошибка при отправке изображения с url:  "+
        imgUrlFromReply+" :(\nПричина ошибки:\n{0}".format(err),  disable_web_page_preview=True)

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
    msgId = update.callback_query.message.reply_to_message.message_id
    chatId = update.callback_query.message.chat.id

    query = update.callback_query
    query.answer()
    msgType = eval(query.data)
    receivedTagListNum =  int(msgType["tagsListNumber"])
    msgType = msgType["tag"].split('_')

    print("Inputted tag: "+msgType[1])
    if (len(msgType) < 2):
        return

    if (msgType[1] != 'end'): # false only tag is servce_end
        if (msgType[0] == 'answ' and msgType[1] == 'false'):
            bot.delete_message(groupId, update.callback_query.message.message_id)
            return
        
        if (msgType[0] != 'service'):
            if (receivedTagListNum == 2): # 2 - rating. Tag was be unique
                tagList = db.getAnswers(tagColumnId)
                for tag in tagList:
                    if tag == "safe" or tag == "suggestive" or tag == "questionable" or tag == "explicit":
                         db.deleteTag(chatId, msgId,tag)
                db.insertAnswer(tagColumnId,  msgType[1])

            else:
                db.insertAnswer(tagColumnId,  msgType[1])

        if (msgType[0] == 'service'):
            keyboardMessageString = ""
            num = 0
            buttonInLine = 0
            if (msgType[1] == 'next'):
                num = receivedTagListNum + 1
            elif (msgType[1] == 'prev'):
                num = receivedTagListNum  - 1

            if num == 1:
                keyboardMessageString = "Выберите теги"
                buttonInLine = 1
            elif num == 2:
                keyboardMessageString = "А ты хорош :3 Теперь выбери рейтинг"
                buttonInLine = 3
            elif num == 3:
                keyboardMessageString = "Молодец :3 Теперь выбери цвет."
                buttonInLine = 3
            elif num == 4:
                keyboardMessageString = "Выбирай ❗➡️ДОПОЛНИТЕЛЬНЫЕ⬅️❗ цвета"
                buttonInLine = 4
            elif num == 5:
                keyboardMessageString = "А кто еще, кроме драконов, есть на изображении?"
                buttonInLine = 3
            elif num == 6:
                keyboardMessageString = "Продолжаем. Вот еще кучка популярных тегов. Что бы закончить жми END ✅"
                buttonInLine = 3
            elif num == 7:
                keyboardMessageString = "Есть еще кучка тегов дальше➡️. Что бы закончить жми END ✅"
                buttonInLine = 3
            elif num == 8:
                keyboardMessageString = "Молодец! А теперь можно перейти в галерею"
                buttonInLine = 3


            keyboard =  tagKeyboard.updateKeyboard(num, buttonInLine)
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(keyboardMessageString, reply_markup=reply_markup)

    # конец выбора
    if (msgType[0] == 'service' and msgType[1] == 'end'):
        tagList = db.getAnswers(tagColumnId)
        ret = APIdrakony.imgSend(imgUrlFromReply, tagList, fromUserSenderIName)
        if (ret):
            bot.delete_message(chatId, msgId)
            bot.delete_message(chatId, update.callback_query.message.message_id)
            bot.send_message(chatId, fromUserSenderIName+" сорян соряныч :( Произошла ошибка при отправке изображения с url:  "+
            imgUrlFromReply+" :(\nПричина ошибки:\n"+ ret, 
             disable_web_page_preview=True)
            db.deleteOnKind(msgId,  chatId)
            return 
        
        philomenaUrl=""
        with open('config.json') as config_file:
            config = json.load(config_file)
        if (config):
            philomenaUrl = config["philomena-url"]
        else:
            logging.error("Error read config file")
            return

        # не уверен нужен ли callback
        keyboard = [[InlineKeyboardButton(
            text="Молодец! А теперь можно перейти в галерею", url=philomenaUrl)]]
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

        if chatIsNSFW(disablePreview, chatId):
            disablePreview = False
                
        replyMsgText += '\n '
        replyMsgText += tagsString
        replyMsgText += "\n Отправлено: "+fromUserSenderIName
        replyMsgText += "\n Галерея: "+artGalleryUrl

        bot.delete_message(chatId, msgId)
        bot.delete_message(chatId, update.callback_query.message.message_id)

        # send message 
        imgPath = htmlUtil.downloadImage(imgUrlFromReply)
        if disablePreview==False and imgPath!="":
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

            imgPath = htmlUtil.downloadImage(imgUrlFromDrakony['Url'])
            
            nsfwTag = False
            if imgUrlFromDrakony['Tags'].find('#explicit') != -1 or   imgUrlFromDrakony['Tags'].find('#questionable') != -1 :
                nsfwTag = True
            
            if (imgUrlFromDrakony and (( nsfwTag or imgPath == "" ) and not chatIsNSFW(True, chatId))):
                msgString = imgUrlFromDrakony['Url']+imgUrlFromDrakony['Tags']+'\nRef: '+imgUrlFromDrakony['UrlToPhilomena']
                bot.send_message(chatId, msgString,  disable_web_page_preview=True)
            else:
                bot.send_chat_action(chatId, 'upload_photo')

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
 
            callbackDataDictTrue = {
            "tagsListNumber":0,
            "tag":"service_next"
            }
            callbackDataDictFalse = {
            "tagsListNumber":0,
            "tag":"answ_false"
            }

            keyboard = [[InlineKeyboardButton("Да", callback_data=str(callbackDataDictTrue)),
                         InlineKeyboardButton("Нет", callback_data=str(callbackDataDictFalse))]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(
                "На изображении есть дракон?", reply_markup=reply_markup)

def main():
    logging.info("Bot started")
    db.createDB()

    config = ""
    with open('config.json') as config_file:
        config = json.load(config_file)

    global artGalleryUrl
    artGalleryUrl = config["philomena-url"]
    token = config["telegram-bot-token"]
    global arrayNSFWchat
    arrayNSFWchat = config["nsfw-chatId"].split(',')
    logger.info("Chat with nsfw: "+str(arrayNSFWchat))

    updater = Updater(
        token, use_context=True)
    global bot
    bot = updater.bot
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(dragonOnImageQuestionWithException))

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
