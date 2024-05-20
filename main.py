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
old_cities = []


@bot.message_handler(commands=["start", "help"])
def start_command(message):
    bot.send_message(message.from_user.id, "Hi")


@bot.message_handler(content_types=["text"])
def start_chatting(message):
    player_city = message.text.lower()
    pprint(gc.search_cities(player_city, case_sensitive=False, contains_search=False))

    if not gc.search_cities(player_city, case_sensitive=False, contains_search=False) or player_city in old_cities:
        bot.send_message(message.from_user.id, "Такого города нет или он уже был")
        return
    if len(old_cities):
        pl_first_letter = old_cities[-1][-1]
        if player_city[0] != pl_first_letter:
            bot.send_message(message.from_user.id, "Не та буква в начале")
            return
    old_cities.append(player_city)
    first_let = player_city[-1]

    if first_let == "ь" or first_let == "ы" or first_let == "ъ":
        first_let = player_city[-2]
    bot.send_message(message.from_user.id, f"Мне на {first_let}")
    bot.send_message(message.from_user.id, search_city(first_let))
    print(old_cities)


def search_city(first_let):
    for cities in all_cities:
        bot_city = all_cities[cities]['alternatenames']
        for c in bot_city:
            if c and c[0] == first_let.upper()[0] and c.lower() not in old_cities:
                old_cities.append(c.lower())
                return c


bot.infinity_polling(timeout=20)

"""
Загуглить: "как обработать геолокацию в телебот пайтон" (чекнуть видосик на ютубе 5-и минутный)
Нужно реализовать так:
зайти с телефона и отправить гео в бота, а он должен просто отпринтовать координаты

2. сделать так, чтобы бот сам отправлял рандомную локацию)


"""
