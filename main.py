from pprint import pprint

import telebot
import random
import pyautogui
from IDTOKEN import *
import geonamescache
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

bot = telebot.TeleBot(TOKEN)
gc = geonamescache.GeonamesCache()
all_cities = gc.get_cities()

players = {}


@bot.message_handler(commands=["start", "help"])
def start_command(message):
    bot.send_message(message.from_user.id, "Hi")


@bot.message_handler(content_types=["text"])
def start_chatting(message):
    player_city = message.text.lower()

    pprint(gc.search_cities(player_city, case_sensitive=False, contains_search=True))
    if not gc.search_cities(player_city, case_sensitive=False, contains_search=True):
        bot.send_message(message.from_user.id, "Такого города нет")
        return
    first_let = player_city[-1]
    if first_let == "ь" or first_let == "ы" or first_let == "ъ":
        first_let = player_city[-2]
    bot.send_message(message.from_user.id, f"Мне на {first_let}")


def search_city(first_let):
    for cities in all_cities:
        bot_city = all_cities[cities]['alternatenames']
        for c in bot_city:
            if c and c[0] == first_let.upper():
                print(c)


search_city("ы")


bot.infinity_polling(timeout=20)

"""
Загуглить: "как обработать геолокацию в телебот пайтон"
Нужно реализовать так:
зайти с телефона и отправить гео в бота, а он должен просто отпринтовать координаты

2. сделать так, чтобы бот сам отправлял рандомную локацию)

3. Все города, которые хранятся в переменной "c" - сохранять в отдельный список (внутри функции search_city) и затем,
после того, как алгоритм дойдёт до конца - просто получить случайный город из списка и вернуть его + отправить юзеру
"""
