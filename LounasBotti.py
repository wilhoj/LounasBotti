# LounasBotti
# Ville Jussila (wilho / OH8ETB)
# <add your name here>
# https://jkry.org/ouluhack/TelegramEMEBot
# 
# Free as a free beer or something.. 
# use and do what ever you want, i will be pleased if you mention me on credits.
#
#
#


import sys
import time
import telepot
import telepot.helper
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton,ForceReply
from telepot.delegate import (
    per_chat_id, create_open, pave_event_space, include_callback_query_chat_id)
from bs4 import BeautifulSoup
import os
import datetime
import pycurl
import re
import string
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO
import logging
import threading
import Queue
import os.path
import datetime
import glob
import getopt
from random import randint

#setup logging
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()

fileHandler = logging.FileHandler("bot.log")
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

rootLogger.setLevel(logging.INFO)
#get important parameters

TOKEN = False
adminid = False
groupid = -248348290 #lanwan
#groupid = -215004621 #testi


try:
    options, remainder = getopt.getopt(sys.argv[1:], 't:a:h')
except getopt.GetoptError as e:
    print("Usage: LounasBotti.py -t TOKEN -a admin_telegram_id" )
    sys.exit(2)

for opt, arg in options:
    if opt == '-h':
        print("Usage: LounasBotti.py -t TOKEN -a admin_telegram_id")
        sys.exit(1)
    elif opt == '-t':
        TOKEN = arg
    elif opt == '-a':
        adminid = arg
if TOKEN == False:
    print 'TOKEN required'
    print("Usage: LounasBotti.py -t TOKEN -a admin_telegram_id")
    sys.exit(1)
if adminid == False:
    print 'not received admin telegram id. Status updates wont be send for admin'



#this is thread save global dict for online user, key is telegram userid (self.id)
users = telepot.helper.SafeDict()

# class which will be created when someone says something to bot 
class LounasBotti(telepot.helper.ChatHandler):

    #Forcereply object for getting those info from user
    forcereply = ForceReply(force_reply = True)

    def __init__(self, *args, **kwargs):
        super(LounasBotti, self).__init__(*args, **kwargs)
        logging.info( "running init for:"+str(self.id))
        self.idents = []
        self.tempusers = str(users)
        # Retrieve from database
        global users
        self.latestmsg =  datetime.datetime.strptime("201622Oct10:29", '%Y%d%b%H:%M') #TODO: fix something more elegant like now()-2days
        self.reg = False
        self.ready = False
        self.livecq = ""
        self.messages = []
        self.name = "NotSet"
        self.stop_loop = False
        self.loop_running = False
        self.blocked = False # if user has blocked bot
        users[self.id] = (self.id, datetime.datetime.now(), datetime.datetime.now(), self.name, "online")
    def on_chat_message(self, msg):
        #try:
        logging.info( msg)
        print(msg)
        if msg['text'] == "paskaa":
            self.sender.sendMessage('Paskalaari tyhja, odottelemme uutta kuormaa..')
            #bot.sendPhoto(groupid, photo=open(getrandompicture(), 'rb'))
            #self.sender.sendPhoto(photo=open(getrandompicture(), 'rb'))


    def _ask_reply(self,text):
        sent = self.sender.sendMessage(text, reply_markup=self.forcereply)
        logging.info( sent)
        self._editor = telepot.helper.Editor(self.bot, sent)
        self._edit_msg_ident = telepot.message_identifier(sent)
        return sent['text']
    # function wich will be automaticly called when timeout will be reached
    def on__idle(self, event):
        logging.info("idle timeout"+str(self.id))
        #self.stopmessageloop()
        #self.sender.sendMessage('Dear '+self.name+' timeout has been reached. You could always restart chat messaging just saying something for me or by sending /star$
        #self.sender.sendMessage('I know you may need a little time. I will always be here for you.')
        self.close()

    # what to do when intance is shutdown
    def on_close(self, ex):
        logging.info("idle timeout"+str(self.id))
        #self.stopmessageloop()
        # Save to database
        #global users
        #self.sender.sendMessage('bye')
        #users[self.id] = (self.id,users[self.id][1], users[self.id][2], self.call, self.name, self.locator,"offline")


#this is thread save global dict for online user, key is telegram userid (self.id)
users = telepot.helper.SafeDict() 

#Starts actual bot
#bot is basicly listener wich will spawn new Instanse off TelegramEMEBot when some one start private conversation whit bot.
# sets timeout for every instance now 10 000 seconds -> about 3h?
bot = telepot.DelegatorBot(TOKEN, [
    include_callback_query_chat_id(
        pave_event_space())(
            per_chat_id(types=['private','group']), create_open, LounasBotti, timeout=200000),
])


# start bot message_loop(listener) to another thread
def startmessageloop():
    bot.message_loop(run_forever='Listening ...')

q = Queue.Queue()
tgt = threading.Thread(target=startmessageloop)
tgt.daemon = True
tgt.start()

#MessageLoop(bot).run_as_thread()
#print('Listening ...')

#groupid = -248348290 #lanwan
#groupid = -215004621 #testi


def getrandompicture():

    list = glob.glob("/home/wilho/PaskaBotti/kuvat2/*.jpg")
    rnd = (randint(0,len(list)))
    print(list[rnd])
    return list[rnd]

def showrandomnotusedpicture():
    notused = ""
    
    while notused == "":
        used = []
        try:
            with open("/home/wilho/PaskaBotti/used") as file:
                used = [line.strip() for line in file]
        except Exception as e:
            logging.error( "Failed to open used file: "+str(e))

        picture = getrandompicture()

        if picture not in used:
            notused = picture

        if notused != "":
            with open('/home/wilho/PaskaBotti/used', 'a') as file:
                file.writelines(notused)
                file.write('\n')
            return notused
        time.sleep(1)


while True:
    logging.info("sengin message from mainloop:")
    global users
    try:
        #bot.sendMessage(groupid, "harhar")
        bot.sendMessage(adminid, "*keep alive*",disable_notification = True,parse_mode = "Markdown")
        #bot.sendPhoto(groupid, photo=open(showrandomnotusedpicture(), 'rb'))
    except Exception as e:
        logging.error( "could not send message to: " + str(adminid) +": "+str(e))
        
    time.sleep(60*60*24)
    
