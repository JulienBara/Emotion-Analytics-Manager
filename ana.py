#coding=utf-8

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from collections import deque
import logging

version = '1.0'



# Read key
key = open('./key').read().splitlines()[0]

# Basic commands 
def start(bot, update):
    chat_id = update.message.chat_id
    message = 'Bonjour, je suis Emotion Analytics Manager'
    bot.sendMessage(chat_id, text=message)


def emo(bot, update):
    chat_id = update.message.chat_id
    mot = update.message.text
    message = mot
    bot.sendMessage(chat_id, text=message)


########################################

updater = Updater(key)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('startEmotionAnalyticsManager', start))
dispatcher.add_handler(MessageHandler([Filters.text], emo))

updater.start_polling()
updater.idle()
