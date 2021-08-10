import telebot
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup as soup
import re

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

def Scrap(url):

    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    driver.maximize_window()
    driver.get(url)

    sleep(2)
    driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[5]/div[2]/ytd-button-renderer[2]/a').click()

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

@bot.message_handler(regexp='https://www.youtube.com/watch\?v=')
def handle_message(message):
    bot.send_message(message.chat.id, "Wait Please, it will take less than 5 seconds :)")
    url = message.text
    reply = Scrap(url)
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Transcript', 'Stats', 'Back')
    bot.reply_to(message.chat.id, reply, reply_markup=keyboard)
    # if message.text.find('&list=') == True:
    #     for href in hrefs:
    #         youtube_scraper(href)
	# youtube_scraper(href)
    # bot.reply_to(message, 'Function not implemented yet', reply_markup=keyboard)

@bot.message_handler(regexp='Stats')
def handle_message(message):
	bot.reply_to(message, 'Stats:')

@bot.message_handler(regexp='Transcript')
def handle_message(message):
	bot.reply_to(message, 'Transcript:')

@bot.message_handler(regexp='Back')
def handle_message(message):
    send_welcome(message)

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