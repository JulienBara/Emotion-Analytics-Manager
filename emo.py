# coding=utf-8

from telegram.ext import Updater, CommandHandler
import requests
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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
    message = analyse_emotion(mot)
    bot.sendMessage(chat_id, text=message)


# Functions
def analyse_emotion(message: str) -> str:
    url = "https://translate.yandex.net/api/v1.5/tr.json/translate"
    query = {'key': yandexKey,
             'lang': 'en',
             'text': message}

    r = requests.post(url, data=query)

    if r.status_code == 200:
        print(r.status_code)
        print(r.text)
        print(r.json())

        translation = r.json()['text']
        print(translation)

        url = "http://gateway-a.watsonplatform.net/calls/text/TextGetEmotion"
        query = {'apikey': watsonKey,
                 'text': translation,
                 'outputMode': 'json'}

        r = requests.post(url, data=query)
        print(r.status_code)
        print(r.text)
        print(r.json())

        doc_emotions = r.json()['docEmotions']

        # new output
        # i = 1    
        # anger = ""
        # while i < float(doc_emotions['anger']) * 10:
        #     anger += "*"
        #     i += 1

        # i = 1
        # disgust = ""
        # while i < float(doc_emotions['disgust']) * 10:
        #     disgust += "*"
        #     i += 1

        # i = 1
        # fear = ""
        # while i < float(doc_emotions['fear']) * 10:
        #     fear += "*"
        #     i += 1

        # i = 1
        # joy = ""
        # while i < float(doc_emotions['joy']) * 10:
        #     joy += "*"
        #     i += 1

        # i = 1
        # sadness = ""
        # while i < float(doc_emotions['sadness']) * 10:
        #     sadness += "*"
        #     i += 1

        # ret = "Colère = " + anger + "\n"\
        #       + "Dégout = " + disgust + "\n"\
        #       + "Peur = " + fear + "\n"\
        #       + "Joie = " + joy + "\n"\
        #       + "Tristesse = " + sadness + "\n"

        # old output

        sum = float(doc_emotions['anger'])\
              + float(doc_emotions['disgust'])\
              + float(doc_emotions['fear'])\
              + float(doc_emotions['fear'])\
              + float(doc_emotions['sadness'])

        ret = "Colère = " + str(round(float(doc_emotions['anger'])/sum, 2)) + "\n"\
              + "Dégout = " + str(round(float(doc_emotions['disgust'])/sum, 2)) + "\n"\
              + "Peur = " + str(round(float(doc_emotions['fear'])/sum, 2)) + "\n"\
              + "Joie = " + str(round(float(doc_emotions['joy'])/sum, 2)) + "\n"\
              + "Tristesse = " + str(round(float(doc_emotions['sadness'])/sum, 2)) + "\n"

    else:
        ret = "Je suis en PLS. Pose cette poule et reviens plus tard. (Status code = " + str(r.status_code) + ")"
    return ret


########################################

updater = Updater(telegramKey)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('startEmo', start))
dispatcher.add_handler(CommandHandler('emo', emo, pass_args=True))

updater.start_polling()
updater.idle()
