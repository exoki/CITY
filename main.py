from pprint import pprint
from datetime import datetime

import telebot
import random
import pyautogui
from IDTOKEN import *
import geonamescache
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests
import wikipedia
import sqlite3


YOUR_API_KEY = "f31f5209-62cd-4326-9606-5b7cddc39993"


bot = telebot.TeleBot(TOKEN)
gc = geonamescache.GeonamesCache()
all_cities = gc.get_cities()

players = {}
old_cities = []


def base():
    with sqlite3.connect("filename.db") as f:
        cursor = f.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS yeat(ID INTEGER, NAME TEXT, USERNAME TEXT, DATE INTEGER)")


base()


def get_players(ID, NAME, USERNAME, DATE):
    with sqlite3.connect("filename.db") as f:
        cursor = f.cursor()
        cursor.execute("""SELECT * FROM yeat WHERE ID =?""", (ID,))
        idbase = cursor.fetchone()
        if idbase is None:
            cursor.execute("""INSERT INTO yeat(ID, NAME, USERNAME, DATE) VALUES(?,?,?,?)""", (ID, NAME, USERNAME, DATE))
        f.commit()


def weather(latitude, longitude):
    answer = requests.get(f"http://api.airvisual.com/v2/nearest_city?lat={latitude}&lon={longitude}&key={YOUR_API_KEY}")
    result = answer.json()
    try:
        aqius = result["data"]["current"]["pollution"]["aqius"]
        hu = result["data"]["current"]["weather"]["hu"]
        tp = result["data"]["current"]["weather"]["tp"]
        ws = result["data"]["current"]["weather"]["ws"]
        return aqius, hu, tp, ws
    except KeyError:
        print(result)
        return None, None, None, None


@bot.message_handler(commands=["game"])
def game(message):
    city, lat, long = search_city(random.choice(list("абвгдеёжзийклмнопрстуфхцчшщыэюя")))
    bot.send_message(message.from_user.id, city)


@bot.message_handler(commands=["start", "help"])
def start_command(message):
    bot.send_message(message.from_user.id, "Hi")
    print(message.from_user)
    get_players(ID=message.from_user.id, NAME=message.from_user.first_name, USERNAME=message.from_user.username, DATE=datetime.now())


@bot.message_handler(content_types=["text"])
def start_chatting(message):
    player_city = message.text.lower()
    pprint(gc.search_cities(player_city, case_sensitive=False, contains_search=False))
    founded = gc.search_cities(player_city, case_sensitive=False, contains_search=False)
    if not founded or player_city in old_cities:
        bot.send_message(message.from_user.id, "Такого города нет или он уже был")
        return
    if len(old_cities):
        pl_first_letter = old_cities[-1][-1]
        if player_city[0] != pl_first_letter:
            bot.send_message(message.from_user.id, "Не та буква в начале")
            return
    old_cities.append(player_city)
    bot.send_location(message.from_user.id, founded[0]["latitude"], founded[0]["longitude"])
    aqius, hu, tp, ws = weather(founded[0]["latitude"], founded[0]["longitude"])
    first_let = player_city[-1]

    if first_let == "ь" or first_let == "ы" or first_let == "ъ":
        first_let = player_city[-2]

    if aqius is not None:
        bot.send_message(message.from_user.id, f"aAQI: {aqius} \nTemp: {tp} \nWS: {ws} \nHU: {hu}")

    bot.send_message(message.from_user.id, f"Мне на {first_let}")

    bot_city, lat_bot, lon_bot = search_city(first_let)
    aqius, hu, tp, ws = weather(lat_bot, lon_bot)
    bot.send_message(message.from_user.id, bot_city)
    if aqius is not None:
        bot.send_message(message.from_user.id, f"aAQI: {aqius} \nTemp: {tp} \nWS: {ws} \nHU: {hu}")
    bot.send_location(message.from_user.id, lat_bot, lon_bot)
    wikipedia.set_lang("ru")
    bot.send_message(message.from_user.id, wikipedia.summary(player_city))
    print(old_cities)


def search_city(first_let):
    for cities in all_cities:
        bot_city = all_cities[cities]['alternatenames']
        for c in bot_city:
            if c and c[0] == first_let.upper()[0] and c.lower() not in old_cities:
                old_cities.append(c.lower())
                return c, all_cities[cities]["latitude"], all_cities[cities]["longitude"]


bot.infinity_polling(timeout=20, skip_pending=True)

"""
Сделать функцию для сброса городов
Сделать функцию, которая напомнит на какую букву нужно говорить (если это вообще надо ахаха)
Не забыть бота на серваке оффнуть, если будешь делать что0то здесь)



"""
