import telebot
import random
import pyautogui
from IDTOKEN import *
import geonamescache
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

bot = telebot.TeleBot(TOKEN)

gc = geonamescache.GeonamesCache()

players = {}


@bot.message_handler(commands=["start", "help"])
def start_command(message):
    bot.send_message(message.from_user.id, "Hi")


@bot.message_handler(content_types=["text"])
def start_chatting(message):
    player_city = message.text
    print(gc.search_cities(player_city, case_sensitive=True, contains_search=True))


bot.infinity_polling(timeout=20)

"""
Загуглить: "как обработать геолокацию в телебот пайтон"
Нужно реализовать так:
зайти с телефона и отправить гео в бота, а он должен просто отпринтовать координаты

2. сделать так, чтобы бот сам отправлял рандомную локацию)
"""
