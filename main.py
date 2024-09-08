import requests
import telebot
from telebot import types
import user_agent
from bs4 import BeautifulSoup
import csv


bot = telebot.TeleBot('')
with open("rootlist.txt") as file:
    whitelist = ([row.strip() for row in file])
print(whitelist)


def weather_now():
    url = "https://www.pogoda.com/saint-petersburg.htm"
    r = requests.get(url)
    #print(r.text)
    bs = BeautifulSoup(r.text, "lxml")
    temp = bs.find_all("span", class_="dato-temperatura changeUnitT")
    #print(temp)
    for temp in temp:
        temp_now = (temp.get("data"))
    temp_now = str(temp_now).replace("|0|","°C")
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


weather_now()


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Погода сейчас")
    btn2 = types.KeyboardButton("❓ Прогноз на 3 дня")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name} {0.last_name}!\nЯ - Ботик, твой персональный метеоролог 😎".format(
                         message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "👋 Погода сейчас"):
        bot.send_message(message.chat.id, text=weather_now())
    elif (message.text == "❓ Прогноз на 3 дня"):
        bot.send_message(message.chat.id, text="WOL еще не готов😭, однако я над этим работаю не покладая лапок💪")
    else:
        bot.send_message(message.chat.id, 'Я тупенькая я не понимаю тебя!')


bot.polling(none_stop=True)
