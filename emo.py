#coding=utf-8

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from collections import deque
import requests
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

version = '1.0'

# Read keys
telegramKey = open('./key').read().splitlines()[0]
yandexKey = open('./yandexKey').read().splitlines()[0]
watsonKey = open('./apikey').read().splitlines()[0]

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
    url = "https://translate.yandex.net/api/v1.5/tr.json/translate"
    query = { 'key': yandexKey,
              'lang': 'en',
              'text': message}

    r = requests.post(url, data=query)

    if(r.status_code == 200):
        print(r.status_code)
        print(r.text)
        print(r.json())

        translation = r.json()['text']
        print(translation)

        url = "http://gateway-a.watsonplatform.net/calls/text/TextGetEmotion"
        query = { 'apikey': watsonKey,
                'text': translation,
                'outputMode': 'json'}    
        
        r = requests.post(url, data=query)
        print(r.status_code)
        print(r.text)
        print(r.json())

        docEmotions = r.json()['docEmotions']

        # new output
        # i = 1    
        # anger = ""
        # while i < float(docEmotions['anger']) * 10:
        #     anger += "*"
        
        # i = 1
        # disgust = ""
        # while i < float(docEmotions['disgust']) * 10:
        #     disgust += "*"

        # i = 1
        # fear = ""
        # while i < float(docEmotions['fear']) * 10:
        #     fear += "*"

        # i = 1
        # joy = ""
        # while i < float(docEmotions['joy']) * 10:
        #     joy += "*"

        # i = 1
        # sadness = ""
        # while i < float(docEmotions['sadness']) * 10:
        #     sadness += "*"

        # ret = "Colère = " + anger + "\n" + "Dégout = " + disgust + "\n" + "Peur = " + fear + "\n" + "Joie = " + joy + "\n" + "Tristesse = " + sadness + "\n"

        # old output
        ret = "Colère = " + docEmotions['anger'] + "\n" + "Dégout = " + docEmotions['disgust'] + "\n" + "Peur = " + docEmotions['fear'] + "\n" + "Joie = " + docEmotions['joy'] + "\n" + "Tristesse = " + docEmotions['sadness'] + "\n"

    else:
        ret = "Je suis en PLS. Pose cette poule et reviens plus tard. (Status code = " + str(r.status_code) +")"
    return ret


########################################

updater = Updater(telegramKey)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('startEmo', start))
dispatcher.add_handler(CommandHandler('emo', emo, pass_args=True))

updater.start_polling()
updater.idle()
