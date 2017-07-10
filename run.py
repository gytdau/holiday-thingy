from slackbot.bot import Bot
from slackbot.bot import listen_to
from slackbot.bot import respond_to
import google_calendar
import commands
from slackbot_settings import *
import json
import re
import pdb
import nlp
import time
import schedule
import threading
import sys
import logging
from Messenger import Messenger
logging.basicConfig()

blocked = False
last_client = None

@respond_to('(.+)', re.IGNORECASE)
def respond(message, text):
    """
    Handles messages sent to the bot and calls the appropriate command.
    """
    messenger = Messenger(message)

    global last_client
    last_client = message.channel._client

    global blocked
    wait_timer = 0
    while blocked:
        time.sleep(0.5)
        wait_timer += 0.5
        print("Message waiting for " + str(wait_timer) + "s")

    blocked = True
    try:
        processed = nlp.query(message, text)
        intent = processed["result"]["metadata"]["intentName"]
        arguments = processed["result"]["parameters"]
        if intent == "failure":
            commands.failure(messenger)
        if intent == "list":
            commands.list(messenger, arguments)
        if intent == "add":
            commands.add(messenger, arguments)
        if intent == "delete":
            commands.delete(messenger, arguments)
        if intent == "undo":
            commands.undo(messenger)
    except:
        blocked = False
        messenger.reply("Well, I seem to have... broke. Sorry about that.")
        raise

    blocked = False

def daily_list():
    """
    Sends a list of the week's tasks to the appropriate channel.
    """
    global blocked

    wait_timer = 0
    while blocked:
        time.sleep(0.5)
        wait_timer += 0.5
        print("Message waiting for " + str(wait_timer) + "s")

    blocked = True

    messenger = Messenger(last_client, SEND_TO)

    try:
        commands.list(messenger, {'date': '', 'date-period': ''})
    except:
        blocked = False
        raise

    blocked = False

schedule.every().day.at(SEND_AT).do(daily_list)

def main():
    """
    Runs everything.
    """
    print("Beep bloop, starting up the bot...")
    google_calendar.initialize_service()
    schedulerThread = threading.Thread(target=run_scheduler, args=(), kwargs={})
    schedulerThread.start()
    bot = Bot()
    bot.run()



def run_scheduler():
    """
    A loop that handles running the daily list on time.
    """
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
