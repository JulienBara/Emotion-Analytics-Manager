from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import http.client, urllib.request, urllib.parse, urllib.error, base64, sys
import logging
import cv2 as cv
import json

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Read keys
key_telegram = open('./keys/keyTelegram').read().splitlines()[0]
key_yandex_translation = open('./keys/keyYandexTranslation').read().splitlines()[0]
key_ibm_watson_text_to_emotion = open('./keys/keyIbmWatsonTextToEmotion').read().splitlines()[0]
key_microsoft_emotion = open('./keys/keyMicrosoftEmotion').read().splitlines()[0]


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


def emo_image(bot, update):
    chat_id = update.message.chat_id
    file_path = bot.getFile(update.message.photo[len(update.message.photo) - 1].file_id).file_path
    emotions_dict = analyse_emotion_image(file_path)
    if len(emotions_dict) > 0:
        file_path_local = draw_emotions(emotions_dict, file_path)
        bot.sendPhoto(chat_id=chat_id, photo=open(file_path_local, 'rb'))


# Functions
def analyse_emotion(message: str) -> str:
    url = "https://translate.yandex.net/api/v1.5/tr.json/translate"
    query = {'key': key_yandex_translation,
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
        query = {'apikey': key_ibm_watson_text_to_emotion,
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

        sum = float(doc_emotions['anger']) \
            + float(doc_emotions['disgust']) \
            + float(doc_emotions['fear']) \
            + float(doc_emotions['fear']) \
            + float(doc_emotions['sadness'])

        ret = "Colère = " + str(round(float(doc_emotions['anger']) / sum, 2)) + "\n" \
            + "Dégout = " + str(round(float(doc_emotions['disgust']) / sum, 2)) + "\n" \
            + "Peur = " + str(round(float(doc_emotions['fear']) / sum, 2)) + "\n" \
            + "Joie = " + str(round(float(doc_emotions['joy']) / sum, 2)) + "\n" \
            + "Tristesse = " + str(round(float(doc_emotions['sadness']) / sum, 2)) + "\n"

    else:
        ret = "Je suis en PLS. Pose cette poule et reviens plus tard. (Status code = " + str(r.status_code) + ")"
    return ret


def analyse_emotion_image(image_url: str) -> json:
    url = "https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize"

    headers = {'Content-Type': 'application/json',
             'Ocp-Apim-Subscription-Key': key_microsoft_emotion}

    query = {'url': image_url}

    r = requests.post(url, headers=headers, data=json.dumps(query, ensure_ascii=False))

    print(r.status_code)
    print(r.text)
    print(r.json())

    return r.json()


def draw_emotions(emotions_dict, file_path):
    file_path_local = "emo_picture.jpg"
    font = cv.FONT_HERSHEY_SIMPLEX
    urllib.request.urlretrieve(file_path, file_path_local)
    img = cv.imread(file_path_local, cv.IMREAD_COLOR)
    for face in emotions_dict:
        rect = face["faceRectangle"]
        cv.rectangle(img, (rect["left"], rect["top"]), (rect["left"] + rect["width"], rect["top"] + rect["height"]), (0, 255, 0), int(img.shape[0]/500)+1)

        emotions = face["scores"]
        max_score = 0
        max_emotion = "anger"
        for emotion in emotions:
            if emotions[emotion] > max_score:
                max_emotion = emotion
                max_score = emotions[emotion]
        cv.putText(img, max_emotion + ": " + str(max_score), (rect["left"], rect["top"] - 2), font, img.shape[0]/500, (0, 255, 0), int(img.shape[0]/500)+1)
        cv.imwrite(file_path_local, img)

    return file_path_local


########################################

updater = Updater(key_telegram)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('startEmo', start))
dispatcher.add_handler(CommandHandler('emo', emo, pass_args=True))
dispatcher.add_handler(MessageHandler(Filters.photo, emo_image))

updater.start_polling()
updater.idle()
