#!/usr/bin/env python3
import telebot;
import requests;
import imgkit;
import json;
from telebot import apihelper;
import os, time, datetime, re, sys;
from pprint import pprint

from passwd import webuser, webpass, ipamuser, ipampass, admins, proxy, url, TOKEN, HomeDir, mailuser, mailpasswd
from servicedesk import get_ticket, send_teleg
from search_json import search_vm_json # функция поиска 

# check email
from exchangelib import DELEGATE, Account, Credentials
from mailcheck import mailcheck
####

bot = telebot.TeleBot(TOKEN);
apihelper.proxy = proxy

os.popen('stat /proc/1/cmdline') # it's for uptime function

def extract_arg(arg):
    return arg.split()[1:]

def get_screen(url):
    loginurl = 'https://zabbix.phoenixit.ru/index.php'
    logindata = {'autologin' : '1', 'name' : webuser, 'password': webpass, 'enter' : 'Sign in'}
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0', 'Content-type' : 'application/x-www-form-urlencoded'}
    session=requests.session()
    login=session.post(loginurl, params=logindata, headers=headers)
    options = {
        'xvfb': ''
    }
    imgkit.from_string ( session.get(url).text, HomeDir+'out.jpg', css=HomeDir+'dark-theme.css', options=options )

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
    intext = message.text
    print ( "["+str(message.from_user.id)+"]:"+intext )

    if message.text.lower() == "id" or message.text.lower() == "/id":
        bot.send_message(message.chat.id, "You telegramm ID is:")
        bot.send_message(message.chat.id, message.from_user.id)

    if str(message.from_user.id) in admins:

        if message.text.lower() == "gp" or message.text.lower() == "/gp": #get http url screen

           try:
               get_screen(url)
           except Exception as inst:
               #print ( type(inst) )     # the exception instance
               #print ( inst.args )      # arguments stored in .args
               #print ( inst )           # __str__ allows args to printed directly

               #bot.send_message(message.from_user.id, "Error in gen screen, pleas contact to SysAdmin")

               pass

           try:
               foto = open(HomeDir+'out.jpg', 'rb')
               bot.send_photo(message.from_user.id, foto)
           except:
               bot.send_message(message.from_user.id, "Error to send/open image, pleas contact to SysAdmin")

           if os.path.exists(HomeDir+'out.jpg'):
              os.remove(HomeDir+'out.jpg')

        elif re.match( r"^[/]*?ip", intext.lower()):
           if re.match( r"^[/]*?ip\s+\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", intext.lower() ): #get ips hostname from IPAM
             ip = extract_arg(message.text)
             bot.send_message(message.from_user.id, get_vm_hostname(ip))
           else:
             bot.send_message(message.from_user.id, "IP addres is't correct, please use /ip <192.0.0.1>")

        elif message.text.lower() == "uptime" or message.text.lower() == "/uptime":
           dateup = os.popen('stat /proc/1/cmdline|grep Change|awk \'{print $2,$3}\'|sed "s/\..........//"|tr -d "\r\n"').read()
           up = time.mktime((datetime.datetime.now()).timetuple()) - time.mktime(datetime.datetime.strptime(dateup, "%Y-%m-%d %H:%M:%S").timetuple())
           bot.send_message(message.from_user.id, str(datetime.timedelta(seconds=up)) )

        elif re.match( r"^[/]*?vm$", intext.lower()):
            bot.send_message(message.from_user.id, "Please use:\nvm [-ip <IP>\n|-mac <MAC>\n|-note <NOTE>\n|-name <NAME>\n|-esxi <ESXI>\n|-snap $n]" )
        elif re.match( r"^[/]*?vm\s+?-.+", intext.lower()):
            args = extract_arg( intext )
            argsstr = ' '.join(str(e) for e in args)
            search_res = {}
            try:
                search_res = search_vm_json( argsstr )
            except:
                bot.send_message(message.from_user.id, "Error to search: "+intext.lower()+", pleas contact to SysAdmin")

            if len( search_res ) != 0:
                if len( search_res ) < 11:
                    for key, value in search_res.items():
                        if re.search( " -all", intext.lower()):
                            bot.send_message(message.from_user.id, json.dumps( value, sort_keys=True, indent=4) )
                        else:
                            path = ""
                            for k,v in sorted( value['PATH'].items(), reverse=True ):
                                path = path + "/" + v
                            vmres = 'Name: '+value['Name']+'\nStatus: '+value['Status']+'\nNote: '+value['Note']+'\nPath: '+path+'\nguest ip: '+str(value["guest ip"])+'\nguest os: '+value["guest os"]+"\nvcenter: "+value['vcenter']
                            bot.send_message(message.from_user.id, str(vmres) )
                else:
                    bot.send_message(message.from_user.id, "Sorry result is to higth: ["+str(len( search_res ))+"]" )
                    print ( "Sorry result is to higth: ["+str(len( search_res ))+"]" )

            else:
                bot.send_message(message.from_user.id, "No result...")

            #except:
            #    bot.send_message(message.from_user.id, "Error to search: "+intext.lower()+", pleas contact to SysAdmin")

        elif message.text.lower() == "sd" or message.text.lower() == "/sd":

            try:
                tickets = get_ticket()
                if len(tickets) != 0 :
                    for key, value in tickets.items():
                        keyboard = telebot.types.InlineKeyboardMarkup()
                        keyboard.add(telebot.types.InlineKeyboardButton(text=key, url='https://servicedesk.phoenixit.ru/Task/View/'+key) )
                        bot.send_message( message.from_user.id, value, reply_markup=keyboard )
                else:
                    bot.send_message( message.from_user.id, "No open tickets." )
            except:
                text = "Error to get tickets from servicedesk, pleas contact to SysAdmin"
                bot.send_message( message.from_user.id, text )
                print(text)

        elif intext == 'kill':
            bot.send_message(message.from_user.id, "You Kiled me! =( ")
            os.system('kill $PPID')
            quit()

        elif intext = 'cm':
            mailcheck(mailuser, mailpasswd, 5);

        else:
            bot.send_message(message.from_user.id, 'For help only put: "/"')

    else:
        if message.text.lower() != "id" and message.text.lower() != "/id":
            bot.send_message(message.chat.id, 'You do\'t have permission!')
            #bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')

try:
    #bot.polling(none_stop=True, interval=0)
    bot.polling(none_stop=True, interval=0, timeout=60)
except Exception as inst:
    print ( type(inst) )     # the exception instance
    print ( inst.args )      # arguments stored in .args
    print ( inst )           # __str__ allows args to printed directly
