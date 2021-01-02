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

        keyboard = tagKeyboard.updateKeyboard(1,1)
        reply_markup = InlineKeyboardMarkup(keyboard)
        print(keyboard)
        query.edit_message_text("Выберите теги.", reply_markup=reply_markup)
    if (msgType[0] == 'tag'):
        db.insertAnswer(tagColumnId,  msgType[1])
        keyboard =  tagKeyboard.updateKeyboard(2,3)
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("Молодец :3 Теперь выбери цвет.", reply_markup=reply_markup)
    
    if (msgType[0]=='color'  and  msgType[1]!='nextTag' and  msgType[1]!='secondColor') :
        db.insertAnswer(tagColumnId,  msgType[1])

    if (msgType[0]=='color'  and  msgType[1]=='secondColor') :
        keyboard =  tagKeyboard.updateKeyboard(3,3)
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            "Выбирай дополнительные цвета.", reply_markup=reply_markup)

    if (msgType[0] == 'secondColor'):
        db.insertAnswer(tagColumnId,  msgType[1])

    if (msgType[0] == 'color' and msgType[1]=='nextTag'):
        
        keyboard =  tagKeyboard.updateKeyboard(4,1)
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            "А ты хорош :3 Теперь выбери рейтинг.", reply_markup=reply_markup)
    if (msgType[0] == 'rating' or msgType[0] == 'moreTags'):
        if (msgType[1] != 'end' and msgType[1] != 'moreTags2' and msgType[1] != 'prev'):
            db.insertAnswer(tagColumnId,  msgType[1])
        keyboard =  tagKeyboard.updateKeyboard(5,3)
        if (msgType[0] != 'moreTags'  and msgType[1]!='end'):
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                "Продолжаем. Вот еще кучка популярных тегов. Что бы закончить жми END ✅", reply_markup=reply_markup)

    # второй выбор
    if (msgType[1] == 'moreTags2' or msgType[0] == 'moreTags2'):
        if (msgType[1] != 'end' and msgType[1] != 'moreTags3' and msgType[1] != 'moreTags2'):
            db.insertAnswer(tagColumnId,  msgType[1])
        keyboard =  tagKeyboard.updateKeyboard(6,3)

        if (msgType[0] != 'moreTags2' and msgType[1] =='moreTags2'  ):
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                "Есть еще кучка тегов дальше➡️. Что бы закончить жми END ✅", reply_markup=reply_markup)

    # третий выбор
    if (msgType[1] == 'moreTags3' or msgType[0] == 'moreTags3'):
        if (msgType[1] != 'end' and msgType[1] != 'moreTags3' and msgType[1] != 'moreTags2'):
            db.insertAnswer(tagColumnId,  msgType[1])
        keyboard =  tagKeyboard.updateKeyboard(7,3)

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
