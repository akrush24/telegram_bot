#!/usr/bin/env python3
import telebot;
import requests;
import imgkit;
from telebot import apihelper;
import os, time, datetime, re, sys;

from passwd import webuser, webpass, ipamuser, ipampass, admins, proxy, url, TOKEN

HomeDir='/home/'
bot = telebot.TeleBot(TOKEN);
apihelper.proxy = proxy

def extract_arg(arg):
    return arg.split()[1:]

def get_screen(url):
    loginurl = 'https://zabbix.phoenixit.ru/index.php'
    logindata = {'autologin' : '1', 'name' : webuser, 'password': webpass, 'enter' : 'Sign in'}
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0', 'Content-type' : 'application/x-www-form-urlencoded'}
    homecss=HomeDir+'dark-theme.css'
    session=requests.session()
    login=session.post(loginurl, params=logindata, headers=headers) 
    imgkit.from_string ( session.get(url).text, HomeDir+'out.jpg', css=HomeDir+'dark-theme.css' )

def get_vm_hostname(ip):
    try:
        token = requests.post('https://ipam.phoenixit.ru/api/apiclient/user/', auth=(ipamuser, ipampass)).json()['data']['token']
        headers = {'token':token}
    except:
        return('Error login in IPAM system, pleas contact to SysAdmin')

    try:
        search = requests.get(url='https://ipam.phoenixit.ru/api/apiclient/addresses/search/'+ip[0], headers=headers).json()['data'][0]
        return('Hostname: '+search['hostname']+', '+' LastSeen: '+search['lastSeen'])
    except:
        return("No found IP: "+ip[0]+", or error")

@bot.message_handler(commands=['start','help'])
def handle_start_help(message):
    pass

@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text.lower() == "id" or message.text.lower() == "/id":
        bot.send_message(message.chat.id, "You telegramm ID is:")
        bot.send_message(message.chat.id, message.from_user.id)

    if str(message.from_user.id) in admins:

        if message.text.lower() == "gp" or message.text.lower() == "/gp": #get http url screen

           try:
               get_screen(url)
           except:
               #bot.send_message(message.from_user.id, "Error in gen screen, pleas contact to SysAdmin")
               pass

           try:
               foto = open(HomeDir+'out.jpg', 'rb') 
               bot.send_photo(message.from_user.id, foto)
           except:
               bot.send_message(message.from_user.id, "Error to send/open image, pleas contact to SysAdmin")

        elif re.match("^[/]*?ip\s.+", message.text.lower()): #get ips hostname from IPAM 
           ip = extract_arg(message.text)
           bot.send_message(message.from_user.id, get_vm_hostname(ip))

        elif message.text.lower() == "uptime" or message.text.lower() == "/uptime":
           dateup = os.popen('stat /proc/1/cmdline|grep Change|awk \'{print $2,$3}\'|sed "s/\..........//"|tr -d "\r\n"').read()
           up = time.mktime((datetime.datetime.now()).timetuple()) - time.mktime(datetime.datetime.strptime(dateup, "%Y-%m-%d %H:%M:%S").timetuple())
           bot.send_message(message.from_user.id, str(datetime.timedelta(seconds=up)) )

        else:
           bot.send_message(message.from_user.id, "For help please put: /")

    else:
        if message.text.lower() != "id" or message.text.lower() != "/id":
            bot.send_message(message.chat.id, 'You do\'t have permission!')
            bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')


#bot.polling(none_stop=True, interval=0)
bot.polling(none_stop=False, interval=0, timeout=20)
