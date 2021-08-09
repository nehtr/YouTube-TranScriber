import telebot

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

@bot.message_handler(regexp='https://www.youtube.com/watch\?v=')
def handle_message(message):
    # if message.text.find('&list=') == True:
    #     for href in hrefs:
    #         youtube_scraper(href)
	# youtube_scraper(href)
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Transcript', 'Stats', 'Back')
    bot.reply_to(message, 'Function not implemented yet', reply_markup=keyboard)

@bot.message_handler(regexp='Stats')
def handle_message(message):
	bot.reply_to(message, 'Stats:')

@bot.message_handler(regexp='Transcript')
def handle_message(message):
	bot.reply_to(message, 'Transcript:')

@bot.message_handler(regexp='Back')
def handle_message(message):
    send_welcome(message)

bot.polling()