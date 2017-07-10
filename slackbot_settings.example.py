

#
# This is an example configuration.
# Add your own keys and rename it to `slackbot_settings.py`.
#


DEFAULT_REPLY = "If you want me to do something, you should tell me what to do."
ERRORS_TO = "gytdau"

PLUGINS = [
    'slackbot.plugins'
]

API_AI_KEY = "api.ai key"
API_TOKEN = "slack integration api key"

# Small inconsequential note: the bot needs to first be messaged after it starts
# before it can send the daily list. Anyone can message it, and they don't
# have to message it directly, they can just ping it.
SEND_AT = "9:00"
SEND_TO = "pto" # send the week's calendar at 9am to the channel #pto


# Google Calendar configuration:
# If modifying these scopes, delete your previously saved credentials
# located in client_secret.json in this folder 
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'PTO Thingy'
