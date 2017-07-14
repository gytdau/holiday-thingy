# Holiday Thingy
[![Build Status](https://travis-ci.org/gytdau/holiday-thingy.svg?branch=master)](https://travis-ci.org/gytdau/holiday-thingy)
[![Code Climate](https://codeclimate.com/github/gytdau/holiday-thingy/badges/gpa.svg)](https://codeclimate.com/github/gytdau/holiday-thingy)
[![Issue Count](https://codeclimate.com/github/gytdau/holiday-thingy/badges/issue_count.svg)](https://codeclimate.com/github/gytdau/holiday-thingy)

A Slack bot that manages employee PTOs.

I made this during my work experience at Workday.

### Explanation
_What's a PTO?_
> Paid time off or personal time off (PTO) is a policy in some employee handbooks that provides a bank of hours in which the employer pools sick days, vacation days, and personal days that allows employees to use as the need or desire arises.
> - Wikipedia

The bot stores PTOs on Google Calendar, and uses api.ai for it's natural language processing. If you'd like the training data for the api.ai agent, email me, or make your own. (You'll have to run the bot on your own server.)

This project is under the MIT license.

### Getting the thing running
Create a Slack integration (a bot user) on your team, and an api.ai account. Put those keys in `holiday_bot/slackbot_settings.py`.

Before you run it, you should install the code (including your configuration):
```
python setup.py install
```

And then run it like this:
```
python holiday_bot/run.py
```

### Tests
Technically, I suppose you could say this repo has tests. You can run them by:

```
python setup.py test
```
