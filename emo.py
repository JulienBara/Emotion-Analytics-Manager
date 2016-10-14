#coding=utf-8

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from collections import deque
import requests
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

version = '1.0'

# Read keys
key = open('./key').read().splitlines()[0]
email = open('./email').read().splitlines()[0]
password = open('./password').read().splitlines()[0]
apiKey = open('./apikey').read().splitlines()[0]

# Basic commands 
def start(bot, update):
    chat_id = update.message.chat_id
    message = 'Bonjour, je suis Emotion Analytics Manager'
    bot.sendMessage(chat_id, text=message)


def emo(bot, update, args):
    chat_id = update.message.chat_id
    mot = ' '.join(args)
    message = analyseEmotion(mot)
    bot.sendMessage(chat_id, text=message)


# Functions
def analyseEmotion(message: str) -> str:
    url = "http://www.frengly.com/"
    query = { 'src': 'fr',
              'dest': 'en',
              'text': message,
              'email': email,
              'password': password,
              'outformat': 'json'}

    r = requests.post(url, data=query)
    print(r.status_code)
    print(r.text)
    print(r.json())

    translation = r.json()['translation']
    print(translation)

    url = "http://gateway-a.watsonplatform.net/calls/text/TextGetEmotion"
    query = { 'apikey': apiKey,
              'text': translation,
              'outputMode': 'json'}    
    
    r = requests.post(url, data=query)
    print(r.status_code)
    print(r.text)
    print(r.json())

    docEmotions = r.json()['docEmotions']
    ret = "Colère = " + docEmotions['anger'] + "\n" + "Dégout = " + docEmotions['disgust'] + "\n" + "Peur = " + docEmotions['fear'] + "\n" + "Joie = " + docEmotions['joy'] + "\n" + "Tristesse = " + docEmotions['sadness'] + "\n"

    return ret


########################################

updater = Updater(key)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('startEmo', start))
dispatcher.add_handler(CommandHandler('emo', emo, pass_args=True))

updater.start_polling()
updater.idle()
