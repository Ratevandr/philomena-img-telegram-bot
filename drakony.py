import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
import re
from pprint import pprint
import json
import APIdrakony
import db

bot = 0
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def dragonOnImageQuestion(update, context):
    print(type(update))

    fromUserClickedId = update.callback_query.from_user.id
    fromUserClickedIdName = update.callback_query.from_user.username
    fromUserSenderId = update.callback_query.message.reply_to_message.from_user.id
    fromUserSenderIName= update.callback_query.message.reply_to_message.from_user.name
    print (" fromUserClickedId: "+str(fromUserClickedId))
    print (" fromUserSenderId: "+str(fromUserSenderId))
    print (" fromUserClickedId: "+ fromUserClickedIdName)
    print (" fromUserSenderId: "+fromUserSenderIName )
    if (fromUserClickedId != fromUserSenderId):
        bot.answer_callback_query(
            callback_query_id=update.callback_query.id, text="Только "+fromUserSenderIName+" может тыкать на кнопки!", show_alert=False)
        return
    msgId = update.callback_query.message.message_id
    # TODO: replace this to api method
    groupId = update["callback_query"]["message"]["chat"]["id"]
    replyMsgText = update.callback_query.message.reply_to_message.text
    imgUrlFromReply = replyMsgText  # TODO: add url proccesing here
    print("msgId "+str(msgId))
    print("groupId "+str(groupId))
    print("text "+replyMsgText)
    print("from "+str(fromUserClickedId))
    print("userName "+update.callback_query.from_user.username)

    tagColumnId = db.searchMsgWithImgID(msgId,  groupId)

    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    #query.edit_message_text(text="Selected option: {}".format(query.data))
    msgType = query.data
    msgType = msgType.split('_')
    if (len(msgType) < 2):
        return

    if (msgType[0] == 'answ' and msgType[1] == 'false'):
        query.edit_message_text("Ок")
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
            [InlineKeyboardButton("black", callback_data='color_black'),
             InlineKeyboardButton("blue", callback_data='color_blue'),
             InlineKeyboardButton("purple", callback_data='color_purple')],
            [InlineKeyboardButton("bronze", callback_data='color_bronze'),
             InlineKeyboardButton("golden", callback_data='color_golden'),
             InlineKeyboardButton("green", callback_data='color_green'),
             InlineKeyboardButton("silver", callback_data='color_silver')],
            [InlineKeyboardButton("grey", callback_data='color_grey'),
             InlineKeyboardButton("red", callback_data='color_red'),
             InlineKeyboardButton("silver", callback_data='color_silver'),
             InlineKeyboardButton("white", callback_data='color_white')],
            [InlineKeyboardButton("yellow", callback_data='color_yellow'),
             InlineKeyboardButton("rainbow", callback_data='color_rainbow'),
             InlineKeyboardButton("other", callback_data='color_other')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            "Молодец :3 Теперь выбери цвет.", reply_markup=reply_markup)
    if (msgType[0] == 'color'):
        db.insertAnswer(tagColumnId,  msgType[1])
        keyboard = [
            [InlineKeyboardButton("safe", callback_data='rating_safe'),
             InlineKeyboardButton("suggestive", callback_data='rating_suggestive'),
             InlineKeyboardButton("questionable", callback_data='rating_questionable'),
             InlineKeyboardButton("explicit", callback_data='rating_explicit')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            "А ты хорош :3 Теперь выбери рейтинг.", reply_markup=reply_markup)
    if (msgType[0] == 'rating' or msgType[0] == 'moreTags'):
        if (msgType[1] != 'end'):
            db.insertAnswer(tagColumnId,  msgType[1])
        keyboard = [
            [InlineKeyboardButton("solo", callback_data='moreTags_solo'),
             InlineKeyboardButton("photo", callback_data='moreTags_photo'),
             InlineKeyboardButton("traditional art", callback_data='moreTags_tradArt')],
            [InlineKeyboardButton("animated", callback_data='moreTags_animated'),
             InlineKeyboardButton("hug", callback_data='moreTags_hug'),
             InlineKeyboardButton("kissing", callback_data='moreTags_kissing')],
            [InlineKeyboardButton("city", callback_data='moreTags_city'),
             InlineKeyboardButton("cloud", callback_data='moreTags_cloud'),
             InlineKeyboardButton("fire", callback_data='moreTags_fire')],
            [InlineKeyboardButton("forest", callback_data='moreTags_forest'),
             InlineKeyboardButton("mountain", callback_data='moreTags_mountain'),
             InlineKeyboardButton("night", callback_data='moreTags_night')],
            [InlineKeyboardButton("sea", callback_data='moreTags_sea'),
             InlineKeyboardButton("sky", callback_data='moreTags_sky'),
             InlineKeyboardButton("space", callback_data='moreTags_space')],
            [InlineKeyboardButton("stars", callback_data='moreTags_stars'),
             InlineKeyboardButton("male", callback_data='moreTags_male'),
             InlineKeyboardButton("female", callback_data='moreTags_female')],
            [InlineKeyboardButton("herm", callback_data='moreTags_herm'),
             InlineKeyboardButton("breasts", callback_data='moreTags_breasts'),
             InlineKeyboardButton("feathered wings", callback_data='moreTags_feathWings')],
            [InlineKeyboardButton("humanized", callback_data='moreTags_humanized'),
             InlineKeyboardButton("furry", callback_data='moreTags_furry'),
             InlineKeyboardButton("anthro", callback_data='moreTags_anthro'),
             InlineKeyboardButton("human", callback_data='moreTags_human')],
            [InlineKeyboardButton("END ✅", callback_data='moreTags_end')]
        ]
        if (msgType[0] != 'moreTags'):
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                "Продолжаем. Вот еще кучка популярных тегов. Что бы закончить жми END ✅", reply_markup=reply_markup)
    if (msgType[0] == 'moreTags' and msgType[1] == 'end'):
        APIdrakony.imgSend(imgUrlFromReply, db.getAnswers(tagColumnId))
        keyboard =  [[InlineKeyboardButton(text="Перейти в галерею", url="https://art.drakony.net",callback_data="1")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # again search
        res = re.search("(?P<url>https?://[^\s]+)", replyMsgText)
        if (res is not None):
            httpUrlStr = res.group("url")
            imgUrlFromDrakony = APIdrakony.imgSearch(httpUrlStr)

        query.edit_message_text(
            imgUrlFromDrakony,reply_markup=reply_markup)
        msgId = update.callback_query.message.message_id
        # TODO: replace this to api method
        chatId = update["callback_query"]["message"]["chat"]["id"]
        bot.delete_message(chatId, msgId) 

        db.deleteOnKind(msgId,  groupId)


def echo(update, context):
    """Echo the user message."""
    res = re.search("(?P<url>https?://[^\s]+)", str(update.message.text))
    if (res is not None):
        httpUrlStr = res.group("url")
        imgUrlFromDrakony = APIdrakony.imgSearch(httpUrlStr)

        if imgUrlFromDrakony:
            msgId = update.message.message_id
            # TODO: replace this to api method
            chatId = update["message"]["chat"]["id"]
            bot.delete_message(chatId, msgId)
            bot.send_message(chatId, imgUrlFromDrakony)
        else:
            keyboard = [[InlineKeyboardButton("Да", callback_data='answ_true'),
                         InlineKeyboardButton("Нет", callback_data='answ_false')]]

            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(
                "На изображении есть дракон?", reply_markup=reply_markup)


def main():
    """Start the bot."""
    db.createDB()
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    token=""
    updater = Updater(
        token, use_context=True)
    global bot 
    bot = updater.bot
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add ConversationHandler to dispatcher that will be used for handling
    # updates

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("clear", clear))
    dp.add_handler(CallbackQueryHandler(dragonOnImageQuestion))
    #dp.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
