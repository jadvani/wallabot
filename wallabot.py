# -*- coding: utf-8 -*-
__author__ = 'Javier Advani'


from bs4 import BeautifulSoup
import urllib
import requests
import time

#bot telegram 
import telebot
from telebot import types


TOKEN = '***' # Ponemos nuestro Token generado con el @BotFather

knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts


def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print "New user detected, who hasn't used \"/start\" yet"
        return 0


# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)  # register listener

# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:  # if user hasn't used the "/start" command yet:
        knownUsers.append(cid)  # save user id, so you could brodcast messages to all users of this bot later
        userStep[cid] = 0  # save user id and his current "command level", so he can use the "/getImage" command
        bot.send_message(cid, "Hello, stranger, let me scan you...")
        bot.send_message(cid, "Scanning complete, I know you now")
        command_help(m)  # show the new user the help page
    else:
        bot.send_message(cid, "ya me he enterado, no insistas")

    cid = m.chat.id
bot.send_message(cid, "¿Qué estás buscando (insertar espacios como +)?")

@bot.message_handler(func=lambda message: True, content_types=['text'])


# error handling if user isn't known yet
# (obsolete once known users are saved to file, because all users
#   had to use the /start command and are therefore known to the bot)
def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print "New user detected, who hasn't used \"/start\" yet"
        return 0


# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text
#search = raw_input("¿Qué estás buscando (insertar espacios como +)? ")

url1='http://es.wallapop.com/search?kws='
url2='&lat=41.398077&lng=2.170432'
#search = 'bukowski'
url=url1+search+url2


# Realizamos la petición a la web
req = requests.get(url)

r = urllib.urlopen(url1+search+url2).read()
soup = BeautifulSoup(r, "html5lib")


#version de soup que uso
#print type(soup)
#imprimo toda la pagina con prettify
#print soup.prettify()

lobbying = {}
vendedores = soup.find_all("span", class_="seller-name")
#no me hace falta, viene en anuncios 
precios = soup.find_all("span", class_="product-info-price")
anuncios = soup.find_all("div", class_="card-product-product-info");
enlaces_imagen =soup.find_all("img", class_="card-product-image")
enlaces =soup.find_all("a")

#cantidad de vendedores, anuncios y precios deben coincidir

print str(len(vendedores))+" resultados coinciden con "+search


i= 0
k=0
while (i<len(enlaces) and k<len(anuncios)):
	if "item" in enlaces[i]["href"]:
		print "http://wallapop.com"+enlaces[i]["href"]+"\n"
		print(enlaces_imagen[k]["src"]+"\n")
		print anuncios[k].get_text()+"\n"
		print vendedores[k].get_text()+"\n"
		k+=1
		time.sleep(5)

	i+=1
