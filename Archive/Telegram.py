from threading import Timer
import telebot
from selenium import webdriver
from time import sleep
import pandas as pd
from bs4 import BeautifulSoup as soup
import re


TOKEN = '1927446263:AAFT-vN5keyQSa9goCsQC7QcIf6KzPCmEnE'
bot = telebot.TeleBot(TOKEN, parse_mode=None)

driver = webdriver.Chrome(executable_path="chromedriver.exe")
driver.maximize_window()

def Scrap(url):
    
    driver.get(url)

    for v in range(0, 20):
        Scroll = driver.execute_script("window.scrollBy(0,250)")
    for w in range(0, 20):
        Scroll = driver.execute_script("window.scrollBy(0,-250)")
    
    dots=driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[6]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/yt-icon-button/button/yt-icon')
    dots.click()
    sleep(1)
    trans=driver.find_element_by_xpath('/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-menu-popup-renderer/tp-yt-paper-listbox/ytd-menu-service-item-renderer/tp-yt-paper-item/yt-formatted-string')
    trans.click()
    dots_trans = driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[2]/div/div[1]/ytd-engagement-panel-section-list-renderer/div[1]/ytd-engagement-panel-title-header-renderer/div[2]/div[5]/ytd-menu-renderer/yt-icon-button/button/yt-icon')
    dots_trans.click()
    sleep(1)
    timestamps = driver.find_element_by_xpath('/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-menu-popup-renderer/tp-yt-paper-listbox/ytd-menu-service-item-renderer/tp-yt-paper-item/yt-formatted-string')
    timestamps.click()
    sleep(1)

    html = driver.page_source
    page_soup = soup(html, "html.parser")

    Views  = page_soup.find("span",{"class":"short-view-count style-scope ytd-video-view-count-renderer"}).text
    Likes = page_soup.findAll("a",{"class":"yt-simple-endpoint style-scope ytd-toggle-button-renderer"})[0].text
    Dislikes = page_soup.findAll("a",{"class":"yt-simple-endpoint style-scope ytd-toggle-button-renderer"})[1].text
    Lenght = page_soup.find("span",{"class":"ytp-time-duration"}).text
    description = page_soup.find("div",{"id":"description"}).text
    Comments = page_soup.findAll('span', text = re.compile(' Comments'), attrs = {'dir' : 'auto'})[0].findPrevious().text
    Title = page_soup.find("h1",{"class":"title style-scope ytd-video-primary-info-renderer"}).text
    Transcripts = page_soup.findAll("div",{"role":"button"})
    Transcript = ''.join([t.text.strip() + " " for t in Transcripts])

    driver.get("https://www.google.com")
    Info =  {"Title ": Title,"Lenght ": Lenght,"Views ": Views,"Likes ": Likes,"Dislikes ": Dislikes,"Comments ": Comments,"description ": description,"Transcript ": Transcript,}
    return f"TiTle: {Title} \n\nLenght: {Lenght} mins \n\nViews: {Views}\n\nLikes: {Likes} Likes\n\nDislikes: {Dislikes} Dislikes\n\nComments: {Comments} Comments\n\n\nDescription:\n\n  {description} \n\nTranscript\n\n {Transcript} \n\n\n========= End"

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
    reply = Scrap(url)
    bot.send_message(message.chat.id, reply)

bot.polling()