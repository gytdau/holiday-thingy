# Holiday Thingy
A Slack bot that manages employee PTOs.

I made this during my work experience at Workday.

### Explanation
_What's a PTO?_
> Paid time off or personal time off (PTO) is a policy in some employee handbooks that provides a bank of hours in which the employer pools sick days, vacation days, and personal days that allows employees to use as the need or desire arises.
> - Wikipedia

The bot stores PTOs on Google Calendar, and uses api.ai for it's natural language processing. (Unfortunately, you'll have to run it on your own server. But that also means nobody else outside your company will see your data.)

This project is under the MIT license.

### Getting the thing running
Create a Slack integration (a bot user), and an api.ai account. Put those keys in `holiday_bot/slackbot_settings.example.py`, and then rename it to `holiday_bot/slackbot_settings.py` so that your settings will take effect.

Run it like this:
```
python holiday_bot/run.py
```

### Tests
Technically, I suppose you could say this repo has tests. You can run them by:

```
python setup.py test
```
