# %%
from googleapiclient.discovery import build
from bs4 import BeautifulSoup as soup
import requests
import pandas as pd
import os
import telebot
from datetime import datetime 


Key = 'AIzaSyDkZ88vmUxTgV-G9lF2cAPScazuJ2hnbXA'
TOKEN = '1927446263:AAFT-vN5keyQSa9goCsQC7QcIf6KzPCmEnE'
bot = telebot.TeleBot(TOKEN, parse_mode=None)

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


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

def message(message):
    url = f"{message}"
    return url

@bot.message_handler(func=message)
def echo_all(message):
    bot.send_message(message.chat.id, "Wait Please, it will take less than 5 seconds :)")
    url = message.text
    try:
        reply = get_stats(url)
        bot.send_message(message.chat.id, reply)
        if os.path.exists("Captions.txt"):
            doc = open('Captions.txt', 'rb')
            bot.send_document(message.chat.id, doc)  
            doc.close()
    except:
        bot.send_message(message.chat.id, "Something is wrong with your Address, please make sure it's following the following format : https://www.youtube.com/watch?v=TIKSk0kXhSc")
    try:
        os.remove("Captions.txt")
    except:
        pass
    
bot.polling()

