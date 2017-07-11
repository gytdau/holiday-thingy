from slackbot.bot import Bot
from slackbot.bot import listen_to
from slackbot.bot import respond_to
from slackbot_settings import *
import json, re, pdb, nlp, time, schedule, threading, sys, logging, google_calendar, commands
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

    global last_client, blocked
    last_client = message.channel._client

    wait()
    blocked = True
    try:
        processed = nlp.query(messenger.sender_id(), text)
        intent = processed["result"]["metadata"]["intentName"]
        arguments = processed["result"]["parameters"]
        execute_intent(intent, messenger, arguments)
    except:
        blocked = False
        raise

    blocked = False

def daily_list():
    """
    Sends a list of the week's tasks to the appropriate channel.
    """
    wait()
    global blocked
    blocked = True

    messenger = Messenger(last_client, SEND_TO)
    try:
        execute_intent("list", messenger, {'date': '', 'date-period': ''})
    except:
        blocked = False
        raise

    blocked = False

def execute_intent(intent, messenger, arguments):
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

def wait():
    """
    If there's a command currently waiting, only return when it's finished.
    """
    global blocked
    wait_timer = 0
    while blocked:
        time.sleep(0.5)
        wait_timer += 0.5
        print("Message waiting for " + str(wait_timer) + "s")

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
