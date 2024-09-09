import requests
import telebot
from telebot import types
from bs4 import BeautifulSoup
import lxml
import csv
import math


bot = telebot.TeleBot('', parse_mode='HTML')
with open("rootlist.txt") as file:
    whitelist = ([row.strip() for row in file])
print(whitelist)


def weather_now():
    url = "https://www.pogoda.com/saint-petersburg.htm"
    r = requests.get(url)
    bs = BeautifulSoup(r.text, "lxml")
    ### ОБЛАЧНОСТЬ
    clouds = bs.find_all("img", width="64")
    for clouds in clouds:
        clouds_now = (clouds.get("alt"))
    print(clouds_now)

    ### ТЕМПЕРАТУРА
    temp = bs.find_all("span", class_="dato-temperatura changeUnitT")
    for temp in temp:
        temp_now = (temp.get("data"))
    temp_now = str(temp_now).replace("|0|","")
    temp_now = "<b>" + str(int(round(float(temp_now)))) + "°C</b>"
    print(temp_now)

    ### ПО ОЩУЩЕНИЯМ
    temp = bs.find_all("span", class_="sensacion changeUnitT")
    for temp in temp:
        temp_feeling = (temp.get("data"))
    temp_feeling = str(temp_feeling).replace("|0|По ощущениям", "")
    temp_feeling = "По ощущениям " + str(int(round(float(temp_feeling)))) + "°C"
    print(temp_feeling)

    ### ВЕТЕР
    wind = bs.find("img", width="32")
    for wind in wind:
        wind_now = (wind.get("alt"))
        print(wind_now)
    wind = bs.find("span", class_="changeUnitW")
    for wind in wind:
        wind_speed = (wind.get("data"))
        print(wind_speed)

    return(temp_now)


def weather_3days():
    url = "https://www.pogoda.com/saint-petersburg.htm"
    r = requests.get(url)
    #print(r.text)
    bs = BeautifulSoup(r.text, "lxml")
    temp = bs.find_all("li", class_="grid-item dia d1 activo")
    print(temp)
    for temp in temp:
        print(temp.get("max changeUnitT"))


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("⚡️ Погода сейчас")
    btn2 = types.KeyboardButton("🌈 Прогноз на 3 дня")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name} {0.last_name}!\nЯ - Лина, твой персональный метеоролог 😎".format(
                         message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "⚡️ Погода сейчас"):
        bot.send_message(message.chat.id, text=weather_now())
    elif (message.text == "🌈 Прогноз на 3 дня"):
        bot.send_message(message.chat.id, text="Прогноз на 3 дня еще не готов😭, однако я над этим работаю не покладая лапок💪")
    else:
        bot.send_message(message.chat.id, 'Я тупенькая я не понимаю тебя!')


bot.polling(none_stop=True)
