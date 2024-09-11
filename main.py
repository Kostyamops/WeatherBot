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

with open("rootlist.txt") as file:
    whitelist = ([row.strip() for row in file])
file.close()

print(whitelist)

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
    #weather_pack.append(str(clouds_now))
    print(clouds_now)

    ### ВЕТЕР
    # wind = bs.find("img", width="32")
    # for wind in wind:
    #     wind_now = (wind.get("alt"))
    #     print(wind_now)
    # wind = bs.find("span", class_="changeUnitW")
    # for wind in wind:
    #     wind_speed = (wind.get("data"))
    #     print(wind_speed)

    return(weather_pack)


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
        message_lines = weather_now()
        print(len(message_lines), message_lines)
        text = ""
        for i in range(0,len(message_lines)):
            text = text + message_lines[i] + "\n"
        print(text)
        bot.send_message(message.chat.id, text=text)
    elif (message.text == "🌈 Прогноз на 3 дня"):
        bot.send_message(message.chat.id, text="Прогноз на 3 дня еще не готов😭, однако я над этим работаю не покладая лапок💪")
    else:
        bot.send_message(message.chat.id, 'Я тупенькая я не понимаю тебя!')


bot.polling(none_stop=True)
