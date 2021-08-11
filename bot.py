"""
YouTube TranScriber v1.0

@authors:
    - Davide
    - Walid

"""

import telebot
from googleapiclient.discovery import build
from bs4 import BeautifulSoup as soup
import requests
import os
import telebot
from telebot import util
import re

Key = 'AIzaSyDkZ88vmUxTgV-G9lF2cAPScazuJ2hnbXA'
TOKEN = '1911738006:AAE2xewL_2WjHVl2H1DoR4-UN7RL5ZyAhrY'
bot = telebot.TeleBot(TOKEN, parse_mode=None)

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

def get_stats(url):
    try:
        os.remove("Captions.txt")
    except:
        pass
    ID = url[url.find("=")+1:]
    youtube = build('youtube','v3', developerKey=Key)
    Request = youtube.videos().list(part = 'snippet,statistics,contentDetails', id = ID)
    response = Request.execute()
    Captions_raw = requests.get(f"http://video.google.com/timedtext?lang=en&v={ID}")
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
    Captions = [Text.text for Text in captions_html.findAll("text")]
    if Transcript_check == 'true':
        new_file = open("Captions.txt", mode="w", encoding="utf-8")
        new_file.writelines(Captions)
    return f"Title: {Title} \n\nLenght: {Lenght} mins \n\nViews: {Views} Views\n\nLikes: {Likes} Likes\n\nDislikes: {Dislikes} Dislikes\n\nComments: {Comments} Comments\n\n\nDescription:\n\n{description}"

@bot.message_handler(regexp='https://www.youtube.com/watch\?v=')
def handle_message(message):
    bot.reply_to(message, '🚧 Please, wait. Work in progress... 🚧')
    url = message.text
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    try:
        reply = get_stats(url)
        if os.path.exists("Captions.txt"):
            keyboard.row('Show transcription', 'Back')
            bot.send_message(message.chat.id, reply, reply_markup=keyboard)
            bot.send_message(message.chat.id, "✅ The transcription has been saved in the file below ⬇️", reply_markup=keyboard)
            doc = open('Captions.txt', 'rb')
            bot.send_document(message.chat.id, doc)  
            doc.close()
        else:
            keyboard.row('Transcribe', 'Back')
            bot.send_message(message.chat.id, reply, reply_markup=keyboard)
            bot.send_message(message.chat.id, "⚠️ No captions are present in this video! ⚠️", reply_markup=keyboard)
            
    except:
        if re.search('&list=', url) != None:
            keyboard.row('Transcribe', 'Back')
            bot.send_message(message.chat.id, "❌ Link to YouTube playlists are not implemented yet. Please, use the link of the single video instead ❌", reply_markup=keyboard)
        else:
            keyboard.row('Transcribe', 'Back')
            bot.send_message(message.chat.id, "❌ Something is wrong with your address, please make sure you've provided the correct link of a YouTube video. ❌", reply_markup=keyboard)

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
        splitted_text = util.split_string(large_text, 3000)
        for text in splitted_text:
            bot.send_message(message.chat.id, text, reply_markup=keyboard)

@bot.message_handler(regexp='Back')
def handle_message(message):
    send_welcome(message)

bot.polling()