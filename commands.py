import google_calendar
from datetime import *
from dateutil.parser import parse # This parser just makes a guess at what format it is in.
# It could be better for stability to supply the format in advance.
import json
import re
import pdb

undo_queue = {}

def failure(message):
    message.reply("Sorry, I didn't catch that.")
    message.send("Try rephrasing what you said to make it clearer :robot_face:")

def list(message, arguments):

    # Defaults and conversions of arguments
    if arguments['date']:
        that_day = parse(arguments['date'])
        arguments['date-period'] = that_day.strftime('%Y-%m-%d') + "/" + (that_day + timedelta(days=1)).strftime('%Y-%m-%d')

    if not arguments['date-period']:
        arguments['date-period'] = datetime.now().strftime('%Y-%m-%d') + "/" + (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')

    # Converting the date range into something we understand

    dates = arguments['date-period'].split('/')
    start_date = parse(dates[0])
    end_date = parse(dates[1])

    # Fetching the data

    events = google_calendar.list_range(start_date, end_date)
    #message.reply("Looks like there's no PTOs from " + start_date.strftime("%Y %A, %d %B") + " to " + end_date.strftime("%A, %d %B") + ".")
    if len(events) == 0:
        message.reply("Looks like there's no PTOs from " + start_date.strftime("%A, %d %B") + " to " + end_date.strftime("%A, %d %B") + ".")
        return

    days_in_range = max(abs((start_date - end_date).days), abs((end_date - start_date).days))
    days = [[] for day in range(days_in_range)]
    continued = []

    for event in events:
        start = parse(event['start']['date'])
        end = parse(event['end']['date'])

        # It appears that Google Calendar counts end dates to be exclusive, but
        # it disguises that in web application. (Just keep that in mind.)

        now = start_date

        readable_start = start.strftime("%A, %d %B")
        readable_end = end.strftime("%A, %d %B")
        readable_return = (end).strftime("%A, %d %B")
        start_days_offset = (start - now).days
        end_days_offset = (end - now).days

        description = '(' + event['description'] + ')' if 'description' in event else ''
        attachments = {
            'end': {
                'fallback': 'Calendar event',
                'title': event['summary'],
                'footer': description,
                'text': 'Returns from PTO',
                'color': '#2ECC40'
            },
            'oneDay': {
                'fallback': 'Calendar event',
                'title': event['summary'],
                'footer': description,
                'text': 'On PTO for one day',
                'color': '#FF851B'
            },
            'start': {
                'fallback': 'Calendar event',
                'title': event['summary'],
                'footer': description,
                'text': 'Starts PTO until they return on ' + readable_return,
                'color': '#FF4136'
            },
            'continue': {
                'fallback': 'Calendar event',
                'title': event['summary'],
                'footer': description,
                'text': 'Still on PTO from ' + readable_start + ' until they return on ' + readable_return,
                'color': '#0074D9'
            }
        }



        if start_days_offset == end_days_offset:
            if start_days_offset < days_in_range:
                # The one day PTO is within the week.
                days[start_days_offset].append(attachments['oneDay'])
        else:
            if start_days_offset < 0 and end_days_offset >= 0:
                continued.append(attachments['continue'])
            elif start_days_offset < days_in_range:
                # The start is within the week.
                days[start_days_offset].append(attachments['start'])


            if end_days_offset < days_in_range:
                # The end is within the week.
                days[end_days_offset].append(attachments['end'])

    message.send('Here\'s what\'s scheduled from ' + start_date.strftime("%A, %d %B") + " to " + end_date.strftime("%A, %d %B") + ".")

    if continued:
        message.send_attatchments(continued)

    if not days:
        message.send("Looks like there's no PTOs this week.")

    for dayNumber, day in enumerate(days):
        if not day:
            continue

        message.send((start_date + timedelta(days=dayNumber)).strftime("%A, %d %B") +":\n")

        message.send_attatchments(day)

    message.send("That's it!")

def add(message, arguments):
    full_name = message.full_name()

    # Defaults and conversions of arguments
    if arguments['date']:
        that_day = parse(arguments['date'])
        arguments['date-period'] = that_day.strftime('%Y-%m-%d') + "/" + (that_day + timedelta(days=1)).strftime('%Y-%m-%d')

    if not arguments['date-period']:
        message.send("I can't book a PTO for you unless you give me a date or a date period.")
        return

    dates = arguments['date-period'].split('/')
    start_date = dates[0]
    end_date = dates[1]
    readable_start = parse(start_date).strftime("%A, %d %B")
    readable_end = parse(end_date).strftime("%A, %d %B")


    # Prevent duplicates
    events = google_calendar.list_range(parse(start_date), parse(end_date))

    for event in events:
        if event['summary'].lower().strip() == full_name.lower().strip():
            message.reply("Uh oh, it looks like you're already booked to be on PTO at that time:")
            start = parse(event['start']['date'])
            end = parse(event['end']['date'])
            readable_start = start.strftime("%A, %d %B")
            readable_end = end.strftime("%A, %d %B")
            attatchment = {
                'fallback': 'Calendar event',
                'title': event['summary'],
                'text': 'On PTO from ' + readable_start + ' until they return on ' + readable_end,
                'color': '#0074D9'
            }
            message.send_attatchments([attatchment])
            message.send("You could delete this PTO or pick another period to book your PTO on.")
            return


    event = {
      'summary': full_name,
      'description': arguments['reason'],
      'start': {
        'date': start_date
      },
      'end': {
        'date': end_date
      }
    }

    google_calendar.add_event(event)
    message.reply("Done, take a look at what I added:")
    attatchment = {
        'fallback': 'Calendar event',
        'title': event['summary'],
        'text': 'On PTO from ' + readable_start + ' until they return on ' + readable_end,
        'color': '#0074D9'
    }
    if arguments['reason'] != '':
        attatchment['footer'] = arguments['reason']

    message.send_attatchments([attatchment])
    message.reply("You can tell me to undo this.")

    user_id = message.sender_id()
    undo_queue[user_id] = {'action': 'add', 'event': event}

def delete(message, arguments):
    full_name = message.full_name()
    full_name = full_name.lower().strip()

    # Defaults and conversions of arguments
    if arguments['date']:
        that_day = parse(arguments['date'])
        arguments['date-period'] = that_day.strftime('%Y-%m-%d') + "/" + (that_day + timedelta(days=1)).strftime('%Y-%m-%d')

    if not arguments['date-period']:
        arguments['date-period'] = datetime.now().strftime('%Y-%m-%d') + "/" + (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')

    # Converting the date range into something we understand

    dates = arguments['date-period'].split('/')
    start_date = parse(dates[0])
    end_date = parse(dates[1])

    # Fetching the data

    events = google_calendar.list_range(start_date, end_date)

    deleted = 0
    to_recreate = []
    for event in events:
        if event['summary'].lower().strip() == full_name:
            google_calendar.delete_event(event['id'])
            to_recreate.append(event)
            deleted += 1

    if deleted == 0:
        message.reply("I didn't delete anything because I couldn't find any PTOs from you between " + start_date.strftime("%A, %d %B %Y")  + " to " + end_date.strftime("%A, %d %B %Y"))
        return

    message.reply(":wastebasket: Done! I deleted " + str(deleted) + " PTOs from you.")
    message.reply("You can tell me to undo this.")

    user_id = message.sender_id()
    undo_queue[user_id] = {'action': 'delete', 'events': to_recreate}

def undo(message):
    user_id = message.sender_id()
    full_name = message.full_name().lower().strip()

    if user_id not in undo_queue or 'action' not in undo_queue[user_id]:
        message.reply("There's nothing you can undo. You could try to delete or create a PTO instead.")
        return

    to_undo = undo_queue[user_id]
    if to_undo['action'] == 'delete':
        for event in to_undo['events']:
            new_event = {
                'summary': event['summary'],
                'start': event['start'],
                'end': event['end']
            }
            if 'description' in event:
                new_event['description'] = event['description']
            google_calendar.add_event(new_event)
        if len(to_undo['events']) == 1:
            message.reply("Undone! I added the PTO back.")
        else:
            message.reply("Undone! I added " + str(len(to_undo['events'])) + " PTOs back.")


    if to_undo['action'] == 'add':
        event = to_undo['event']
        start_date = parse(event['start']['date'])
        end_date = parse(event['end']['date'])
        events = google_calendar.list_range(start_date, end_date)

        for event in events:
            if event['summary'].lower().strip() == full_name:
                google_calendar.delete_event(event['id'])
                message.reply("Undone! I deleted that PTO.")
                message.reply("If I got something when making it, you could try again but phrase it differently.")
                break
    undo_queue.pop(user_id, None)
