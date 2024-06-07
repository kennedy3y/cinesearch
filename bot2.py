import telebot
from telebot.util import quick_markup
from telebot import types
import pandas as pd

#Change the variable below
BOT_TOKEN = 'YOUR BOT TOKEN' #Add your telegram bot token -> claim bot as yours. [REQUIRED*]
botAdmin = 'YOUR PERSONAL PROFILE LINK (BOT ADMIN)' #Add your personal profile link here -> people can contact you. [REQUIRED*]
bot1 = "FIRST BOT'S LINK (BOT 1)" #Add your bot1 link. -> redirect back to 1st bot. (A Failsafe Protocol) [REQUIRED*]

bot = telebot.TeleBot(BOT_TOKEN)
df = pd.read_csv('ml.csv')


@bot.message_handler(commands=['start'])
def start_message(message):
    text = message.text.split()
    argument = text[1] if len(text) > 1 else None

    if argument:
        result = df[df['CODE'] == argument]
        if not result.empty:
            image = result['IMAGE'].iloc[0]
            title = result['TITLE'].iloc[0]
            year = result['YEAR'].iloc[0]
            language = result['LANGUAGE'].iloc[0]
            duration = result['DURATION'].iloc[0]
            imdbRating = result['IMDBRATING'].iloc[0]
            genres = result['GENRES'].iloc[0]

            quality1FileSize = result['FIRSTQUALITYFILESIZE'].iloc[0]
            quality2FileSize = result['SECONDQUALITYFILESIZE'].iloc[0]
            quality3FileSize = result['THIRDQUALITYFILESIZE'].iloc[0]

            quality1Link = result['FIRSTQUALITYLINK'].iloc[0]
            quality2Link = result['SECONDQUALITYLINK'].iloc[0]
            quality3Link = result['THIRDQUALITYLINK'].iloc[0]

            quality1 = result['FIRSTQUALITY'].iloc[0]
            quality2 = result['SECONDQUALITY'].iloc[0]
            quality3 = result['THIRDQUALITY'].iloc[0]

            quality1Button = types.InlineKeyboardButton(text=quality1, url=quality1Link)
            quality2Button = types.InlineKeyboardButton(text=quality2, url=quality2Link)
            quality3Button = types.InlineKeyboardButton(text=quality3, url=quality3Link)

            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(quality1Button, quality2Button, quality3Button)

            bot.send_photo(message.chat.id, image)
            bot.send_message(message.chat.id, f'☘️ {title} ({year})\n🗣 Language : {language}\n🕰️ Duration: {duration}\n🏆 IMDB Rating : {imdbRating}\n🎭 Genres : {genres}\n\n{quality1} | {quality2} | {quality3} \n{quality1FileSize} | {quality2FileSize} | {quality3FileSize}', reply_markup=markup)
        else:
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton(text="Noo! I want a film you don't have right now!", url=botAdmin))

            bot.send_message(message.chat.id, "Sir, did you tried to bypass something? 😐", reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(text='Oh! ok! I want the movie called...', url=bot1))

        bot.send_message(message.chat.id, 'Sir, please select the movie before coming here! 😊', reply_markup=markup)

bot.polling()