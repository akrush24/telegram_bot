#!/usr/bin/env python3
from telebot import apihelper, TeleBot
#import config
from passwd import TOKEN, admins, proxy

apihelper.proxy = proxy
bot = TeleBot(TOKEN)
chat_id=admins[0]
bot.send_message(chat_id, 'Wake up!')
