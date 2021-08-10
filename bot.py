import telebot
from googleapiclient.discovery import build
from bs4 import BeautifulSoup as soup
import requests
import pandas as pd
import os
import telebot
from datetime import datetime 

Key = 'AIzaSyDkZ88vmUxTgV-G9lF2cAPScazuJ2hnbXA'
TOKEN = '1911738006:AAE2xewL_2WjHVl2H1DoR4-UN7RL5ZyAhrY'
bot = telebot.TeleBot(TOKEN, parse_mode=None)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Transcribe', 'Help')
    bot.reply_to(message, 'Select an option', reply_markup=keyboard)

@bot.message_handler(regexp='Transcribe')
def handle_message(message):
    keyboard = telebot.types.ReplyKeyboardRemove(selective=True)
    bot.reply_to(message, 'Please, insert the link of the video:', reply_markup=keyboard)

@bot.message_handler(regexp='Help')
def handle_message(message):
	bot.reply_to(message, 'Text not implemented yet') # TO DO

def get_stats(url):
    a = datetime.now()
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

    Captions = str([Text.text for Text in captions_html.findAll("text")])
    
    if Transcript_check == 'true':
        pd.DataFrame([Captions]).to_csv("Captions.txt")
        result_caption = " Please Check the file sent to you"
    else:
        result_caption = " No Captions were found sorry :'("
        
    b = datetime.now()

    execution_time = (b - a).seconds
    return f"It took {execution_time} seconds to execute.\n\nTiTle: {Title} \n\nLenght: {Lenght} mins \n\nViews: {Views} Views\n\nLikes: {Likes} Likes\n\nDislikes: {Dislikes} Dislikes\n\nComments: {Comments} Comments\n\n\nDescription:\n\n{description}\n\nCaptions:{result_caption} ========= End"

def message(message):
    url = f"{message}"
    return url

@bot.message_handler(regexp='https://www.youtube.com/watch\?v=')
def handle_message(message):
    url = message.text
    try:
        reply = get_stats(url)
        bot.send_message(message.chat.id, reply)
        if os.path.exists("Captions.txt"):
            doc = open('Captions.txt', 'rb')
            bot.send_document(message.chat.id, doc)  
            doc.close()
    except:
        bot.send_message(message.chat.id, "Something is wrong with your Address, please make sure you've provided the correct link of a YouTube video")
    try:
        os.remove("Captions.txt")
    except:
        pass
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Show transcript', 'Back')

    # if message.text.find('&list=') == True:
    #     for href in hrefs:
    #         youtube_scraper(href)
	# youtube_scraper(href)
    # bot.reply_to(message, 'Function not implemented yet', reply_markup=keyboard)

@bot.message_handler(regexp='Show transcript')
def handle_message(message):
	bot.reply_to(message, 'Not implemented yet')

@bot.message_handler(regexp='Back')
def handle_message(message):
    send_welcome(message)

bot.polling()