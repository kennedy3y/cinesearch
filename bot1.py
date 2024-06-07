import telebot
import requests
import txtai
import numpy as np
import pandas as pd
from telebot.util import quick_markup
from telebot import types
import itertools

#Change the variable below
BOT_TOKEN = 'YOUR BOT TOKEN' #Add your telegram bot token -> claim bot as yours [REQUIRED*]
botAdmin = 'YOUR PERSONAL PROFILE LINK (BOT ADMIN)' #Add your personal profile link here -> people can contact you. [REQUIRED*]


bot = telebot.TeleBot(BOT_TOKEN)
df = pd.read_csv('ml.csv')

titles = df.TITLE.values
qualityLinks = df.QUALITYLINK.values


embeddings = txtai.Embeddings({
    'path': 'sentence-transformers/all-MiniLM-L6-v2'
})

embeddings.index(titles)

embeddings.save('embeddings.tar.gz')

@bot.message_handler(commands=['start'])
def send_welcome(message):
  bot.reply_to(message, "<b>😍  Hey sir! I'm a Movie Bot.\n\n🫡  I'll give you any movie you want! You just have to tell me the movie name.\n🏃‍♀️  You can download it through telegram without leaving\n\n🫶  480p, 720p, 1080 and many other Qualities are available!\n\n❤️‍🔥\n👀 So, what are you waiting for?</b>", parse_mode='HTML')

@bot.message_handler(func=lambda message: True)
def boot(message):
  result = embeddings.search(query= message.text, limit= 5)
  actualTitleResults = [titles[x[0]] for x in result]
  actualQualityLinkResults = [qualityLinks[x[0]] for x in result]

  markup = types.InlineKeyboardMarkup(row_width=1)

  for title, qualityLink in zip(actualTitleResults, actualQualityLinkResults):
    markup.add(types.InlineKeyboardButton(text=title, url=qualityLink))

  markup.add(types.InlineKeyboardButton(text= "Don't see the film you want? 😔", url=botAdmin))

  bot.reply_to(message, 'Here you go! 😊', reply_markup=markup)

bot.infinity_polling()