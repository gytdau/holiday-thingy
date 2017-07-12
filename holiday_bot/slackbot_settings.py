DEFAULT_REPLY = "Hi! :wave: If you want me to do something, you should tell me what to do."
ERRORS_TO = "gytdau"

PLUGINS = [
    'slackbot.plugins'
]

API_AI_KEY = "054f44ee85f344c4a29a9e8b32d988b8"
API_TOKEN = "xoxb-207907785414-UrVq0Fr75aE8nQvb4qXDUV5h"

# Small inconsequential note: the bot needs to first be messaged after it starts
# before it can send the daily list. Anyone can message it, and they don't
# have to message it directly, they can just ping it.
SEND_AT = "11:44"
SEND_TO = "pto"


# Google Calendar configuration:
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'PTO Thingy'
