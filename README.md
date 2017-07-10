# PTO Thingy
A Slack bot that manages employee PTOs.

It stores PTOs on Google Calendar, and uses api.ai for it's natural language processing.

### Getting the thing running
Create a Slack integration (a bot user), and an api.ai account. Put those keys in `slackbot_settings.example.py`, and then rename it to `slackbot_settings.py`.

Run it like this:
```
python run.py
```
