import requests
import telebot
from telebot import types
from bs4 import BeautifulSoup
import lxml
import csv
import math


with open("token.txt") as file:
    bot = telebot.TeleBot(file.readline(), parse_mode='HTML')
file.close()


def clouds_emoji(clouds_now):
    clouds_now = clouds_now.lower()
    if "дождь" in clouds_now:
        return("🌧")
    elif "небольшой дождь" in clouds_now:
        return("🌦")
    elif "пасмурно" in clouds_now:
        return ("☁️")
    elif "переменная облачность" in clouds_now:
        return("🌥")
    elif "малооблачно" in clouds_now:
        return("⛅️")
    elif "облачно и ясно" in clouds_now:
        return("🌤")
    elif "солнечно и ясно" in clouds_now:
        return("☀️")
    elif "ясное небо" in clouds_now:
        return("☀️")
    elif "снег" in clouds_now:
        return("🌨")
    elif "мокрый снег" in clouds_now:
        return("🌨")
    elif "грязь с пылью" in clouds_now:
        return("🌫")
    elif "туман" in clouds_now:
        return("🌫")
    elif "дымка" in clouds_now:
        return("🌫")
    elif "гроза" in clouds_now:
        return("⛈")
    else:
        return("|")


def replace_temp_symbols(temp):
    temp_pack = []
    for i in range(0, len(temp)):
        new_temp = str(temp[i])
        new_temp = new_temp.replace('<span class="t">', "")
        new_temp = new_temp.replace('</span>', "")
        new_temp = new_temp.replace('°', "")
        new_temp = new_temp.replace('+', "")
        new_temp = new_temp.replace('...', " ")
        temp_pack.append(list(map(str, new_temp.split())))
    return(temp_pack)


def replace_clouds_symbols(clouds):
    clouds_pack = []
    for i in range(0, len(clouds)):
        new_clouds = str(clouds[i])
        new_clouds = new_clouds.replace('<div class="cl_title">', "")
        new_clouds = new_clouds.replace('<br/>', "+")
        new_clouds = new_clouds.replace('</div>', "")
        new_clouds = new_clouds[0].upper() + new_clouds[1::]
        clouds_pack.append(list(map(str, new_clouds.split("+"))))
    return(clouds_pack)


def weather_now():
    weather_pack = []
    url = "https://www.pogoda.com/saint-petersburg.htm"
    r = requests.get(url)
    bs = BeautifulSoup(r.text, "lxml")

    ### ТЕМПЕРАТУРА
    temp = bs.find_all("span", class_="dato-temperatura changeUnitT")
    for temp in temp:
        temp_now = (temp.get("data"))
    temp_now = str(temp_now).replace("|0|","")
    temp_now = "<b>" + str(int(round(float(temp_now)))) + "°C</b>"
    weather_pack.append(str(temp_now))
    print(temp_now)

    ### ПО ОЩУЩЕНИЯМ
    temp = bs.find_all("span", class_="sensacion changeUnitT")
    for temp in temp:
        temp_feeling = (temp.get("data"))
    temp_feeling = str(temp_feeling).replace("|0|По ощущениям", "")
    temp_feeling = "<i>" + "По ощущениям " + str(int(round(float(temp_feeling)))) + "°C" + "</i>"
    weather_pack.append(str(temp_feeling))
    print(temp_feeling)
    
    ### ОБЛАЧНОСТЬ
    clouds = bs.find_all("img", width="64")
    for clouds in clouds:
        clouds_now = (clouds.get("alt"))
    weather_pack[0] = weather_pack[0] + " " + clouds_emoji(clouds_now) + " " + str(clouds_now)
    print(clouds_now)

    return(weather_pack)


def weather_3days():
    weather_pack = []
    url = "https://spb.nuipogoda.ru/погода-на-14-дней"
    r = requests.get(url)
    bs = BeautifulSoup(r.text, "lxml")

    ### ТЕМПЕРАТУРА
    temp = bs.find_all("span", class_="t")
    temp_2weeks = replace_temp_symbols(temp)
    print(temp_2weeks)

    ### ОБЛАЧНОСТЬ
    clouds = bs.find_all("div", class_="cl_title")
    clouds_2weeks = replace_clouds_symbols(clouds)
    print(clouds_2weeks)

    weather_pack_3days = []
    weather_pack_3days.append("✨Завтра")
    weather_pack_3days.append("<b>" + temp_2weeks[1][0] + "°C - " + temp_2weeks[1][1] + "°C</b>")
    weather_pack_3days.append("<i>" + clouds_2weeks[1][0] + ", " + clouds_2weeks[1][1] + "</i>")
    weather_pack_3days.append("")
    weather_pack_3days.append("✨Послезавтра")
    weather_pack_3days.append("<b>" + temp_2weeks[2][0] + "°C - " + temp_2weeks[2][1] + "°C</b>")
    weather_pack_3days.append("<i>" + clouds_2weeks[2][0] + ", " + clouds_2weeks[2][1] + "</i>")
    weather_pack_3days.append("")
    weather_pack_3days.append("✨Через 2 дня")
    weather_pack_3days.append("<b>" + temp_2weeks[3][0] + "°C - " + temp_2weeks[3][1] + "°C</b>")
    weather_pack_3days.append("<i>" + clouds_2weeks[3][0] + ", " + clouds_2weeks[3][1] + "</i>")

    return(weather_pack_3days)


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
        message_lines = weather_now()
        print(len(message_lines), message_lines)
        text = ""
        for i in range(0,len(message_lines)):
            text = text + message_lines[i] + "\n"
        print(text)
        bot.send_message(message.chat.id, text=text)
    elif (message.text == "🌈 Прогноз на 3 дня"):
        message_lines = weather_3days()
        print(len(message_lines), message_lines)
        text = ""
        for i in range(0, len(message_lines)):
            text = text + message_lines[i] + "\n"
        print(text)
        bot.send_message(message.chat.id, text=text)
    else:
        bot.send_message(message.chat.id, 'Я тупенькая я не понимаю тебя!')


bot.polling(none_stop=True)
