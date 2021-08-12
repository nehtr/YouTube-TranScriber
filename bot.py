"""
YouTube TranScriber v1.1

@authors:
    - Davide
    - Walid

@contributors:
    - Sivareddy

"""

import telebot
from googleapiclient.discovery import build
from bs4 import BeautifulSoup as soup
import requests
import os
import telebot
import re
import bcp47

Key = 'AIzaSyDkZ88vmUxTgV-G9lF2cAPScazuJ2hnbXA'
# TOKEN = '1911738006:AAE2xewL_2WjHVl2H1DoR4-UN7RL5ZyAhrY'
TOKEN = '1804086945:AAFbhluZ2A0hrvB2w4Ki6HO_ZsyIxeaBrZ8'
bot = telebot.TeleBot(TOKEN, parse_mode=None)

url = ""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Transcribe', 'Help')
    bot.reply_to(message, '📝 Welcome to YouTube TranScriber 1.0! 📝\n\nSelect an option', reply_markup=keyboard)

@bot.message_handler(regexp='Transcribe')
def handle_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Help')
    bot.reply_to(message, 'Please, insert the link of the video:', reply_markup=keyboard)

@bot.message_handler(regexp='Help')
def handle_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Transcribe')
    bot.reply_to(message, '''
❓ Help ❓

With this bot you can get the stats and entire transcription of a video.
The program is a work in progress, so please report any bugs or requests.

The program suits particularly to the podcast videos, but it can be used for any video with a caption.
To get the captions of a video you just have to click on the "Transcribe" button and insert the link of the video.
The program will automatically get the stats and the captions of the video, providing the first one in a message and the last one in a file.
If you want to see the entire transcription directly inside Telegram, just click the "Show transcription" button.

When inserting the link of the video, pay attention to not insert a link to a playlist or channel, since the transcription from those links is not supported yet.

Thanks for the use of this program and have fun! 😊
    ''', reply_markup=keyboard)

def get_languages(url):
    ID = url[url.find("=")+1:]
    url = f"http://video.google.com/timedtext?type=list&v={ID}"
    Soup = soup(requests.get(url).content,"html.parser")
    Languages = Soup.findAll("track")
    return {Language["lang_original"] : Language["lang_code"] for Language in Languages}

def get_stats(url, lang='en'):
    try:
        os.remove("Captions.txt")
    except:
        pass
    ID = url[url.find("=")+1:]
    youtube = build('youtube','v3', developerKey=Key)
    Request = youtube.videos().list(part = 'snippet,statistics,contentDetails', id=ID)
    response = Request.execute()
    Captions_raw = requests.get(f"http://video.google.com/timedtext?lang={lang}&v={ID}")
    captions_html = soup(Captions_raw.content, "html.parser")
    Title = response['items'][0]['snippet']['title']
    Views  = response['items'][0]['statistics']['viewCount']
    Likes = response['items'][0]['statistics']['likeCount']
    Dislikes = response['items'][0]['statistics']['dislikeCount']
    Comments = response['items'][0]['statistics']['commentCount']
    Lenght = response['items'][0]['contentDetails']['duration'].replace("PT","").replace("M",":").replace("S","").replace("H",":")
    description = response['items'][0]['snippet']['description']
    Image = response['items'][0]['snippet']['thumbnails']['maxres']['url']
    Transcript_check = response['items'][0]['contentDetails']['caption']
    if Transcript_check == 'true':
        Captions = [Text.text for Text in captions_html.findAll("text")]
        new_file = open("Captions.txt", mode="w", encoding="utf-8")
        new_file.writelines(Captions)
    return f"Title: {Title} \n\nLenght: {Lenght} mins \n\nViews: {Views} Views\n\nLikes: {Likes} Likes\n\nDislikes: {Dislikes} Dislikes\n\nComments: {Comments} Comments\n\n\nDescription:\n\n{description}"

def url_cleaner(url):
    if re.search('&', url) != None:
        url = url[:url.find("&")]
    return url

@bot.message_handler(regexp='https://www.youtube.com/watch\?v=')
def handle_message(message):
    global url
    url = message.text
    url = url_cleaner(url)
    lang_choice = get_languages(url)
    keyboard = telebot.types.InlineKeyboardMarkup()
    for key, value in lang_choice.items():
        keyboard.add(telebot.types.InlineKeyboardButton(text=key, callback_data=value))
    if len(lang_choice) > 0:
        bot.reply_to(message, 'Please, select the language:', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "⚠️ No captions are present in this video! ⚠️", reply_markup=keyboard)
        bot.send_message(message.chat.id, '🚧 Please, wait. Retrieving the statistics... 🚧', reply_markup=keyboard)
        reply = get_stats(url)
        bot.send_message(message.chat.id, reply, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call : call.data in bcp47.languages.values())
def callback_query(call):
    lang = call.data
    bot.send_message(call.message.chat.id, '🚧 Please, wait. Work in progress... 🚧')
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    try:
        reply = get_stats(url, lang)
        bot.send_message(call.message.chat.id, reply, reply_markup=keyboard)
        if os.path.exists("Captions.txt"):
            keyboard.row('Show transcription', 'Back')
            bot.send_message(call.message.chat.id, "✅ The transcription has been saved in the file below ⬇️", reply_markup=keyboard)
            doc = open('Captions.txt', 'rb')
            bot.send_document(call.message.chat.id, doc)
            doc.close()
        else:
            keyboard.row('Transcribe', 'Back')
            bot.send_message(call.message.chat.id, reply, reply_markup=keyboard)
            bot.send_message(call.message.chat.id, "⚠️ No captions are present in this video! ⚠️", reply_markup=keyboard)
    except:
        keyboard.row('Transcribe', 'Back')
        bot.send_message(call.message.chat.id, "❌ Something is wrong with your address, please make sure you've provided the correct link of a YouTube video. ❌", reply_markup=keyboard)

    # if message.text.find('&list=') == True:
    #     for href in hrefs:
    #         youtube_scraper(href)
	# youtube_scraper(href)
    # bot.reply_to(message, 'Function not implemented yet', reply_markup=keyboard)

@bot.message_handler(regexp='Show transcription')
def handle_message(message):
    with open("Captions.txt", "rb") as large_text:
        large_text = large_text.read()
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Transcribe', 'Back')
        splitted_text = telebot.util.split_string(large_text, 3000)
        for text in splitted_text:
            bot.send_message(message.chat.id, text, reply_markup=keyboard)

@bot.message_handler(regexp='Back')
def handle_message(message):
    send_welcome(message)

bot.polling()