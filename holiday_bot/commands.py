from datetime import *
from dateutil.parser import parse # This parser just makes a guess at what format it is in.
# It could be better for stability to supply the format in advance.
import json, re, pdb
from holiday_bot import google_calendar

undo_queue = {}

def failure(message):
    message.reply("Sorry, I didn't catch that.")
    message.send("Try rephrasing what you said to make it clearer :robot_face:")

def list(message, arguments):

    arguments = convert_dates(arguments, 7)
    start_date, end_date = date_period_to_datetime_objects(arguments)

    # Fetching the data

    events = google_calendar.list_range(start_date, end_date)

    if len(events) == 0:
        message.reply("Looks like there's no PTOs from " + readable_format(start_date) + " to " + readable_format(end_date) + ".")
        return

    days_in_range = max(abs((start_date - end_date).days), abs((end_date - start_date).days))
    days = [[] for day in range(days_in_range)]
    continued = []

    for event in events:
        start = parse(event['start']['date'])
        end = parse(event['end']['date'])

        now = start_date

        start_days_offset = (start - now).days
        end_days_offset = (end - now).days

        full_name = event['summary']
        description = None
        if 'description' in event:
            description = event['description']

        if start_days_offset == end_days_offset:
            if start_days_offset < days_in_range:
                # The one day PTO is within the week.
                attachment = generate_attachment(full_name, "oneDay", description, start, end)
                days[start_days_offset].append(attachment)
        else:
            if start_days_offset < 0 and end_days_offset >= 0:
                attachment = generate_attachment(full_name, "continue", description, start, end)
                continued.append(attachment)

            elif start_days_offset < days_in_range:
                # The start is within the week.
                attachment = generate_attachment(full_name, "start", description, start, end)
                days[start_days_offset].append(attachment)

            if end_days_offset < days_in_range:
                # The end is within the week.
                attachment = generate_attachment(full_name, "end", description, start, end)
                days[end_days_offset].append(attachment)

    message.send('Here\'s what\'s scheduled from ' + readable_format(start_date) + " to " + readable_format(end_date) + ".")

    if continued:
        message.send_attachments(continued)

    if not days:
        message.send("It looks like there's no PTOs from " + readable_format(start_date) + " to " + readable_format(end_date) + ".")

    for dayNumber, day in enumerate(days):
        if day:
            message.send(readable_format(start_date + timedelta(days=dayNumber)) +":\n")
            message.send_attachments(day)

    message.send("That's it!")

def add(message, arguments):
    full_name = message.full_name()

    arguments = convert_dates(arguments)

    if not arguments['date-period']:
        message.send("I can't book a PTO for you unless you give me a date or a date period.")
        return

    start_date, end_date = date_period_to_datetime_objects(arguments)

    # Prevent duplicates
    events = google_calendar.list_range(start_date, end_date)

    for event in events:
        if event['summary'].lower().strip() == full_name.lower().strip():
            message.reply("Uh oh, it looks like you're already booked to be on PTO at that time:")
            start = parse(event['start']['date'])
            end = parse(event['end']['date'])
            attachment = generate_attachment(full_name, "future", event['description'] if 'description' in event else '', start, end)
            message.send_attachments([attachment])
            message.send("You could delete this PTO or pick another period to book your PTO on.")
            return


    event = {
      'summary': full_name,
      'description': arguments['reason'],
      'start': {
        'date': iso_format(start_date)
      },
      'end': {
        'date': iso_format(end_date)
      }
    }

    google_calendar.add_event(event)
    message.reply("Done, take a look at what I added:")
    attachment = generate_attachment(full_name, "future", event['description'] if 'description' in event else '', start_date, end_date)
    message.send_attachments([attachment])
    message.reply("You can tell me to undo this.")

    user_id = message.sender_id()
    undo_queue[user_id] = {'action': 'add', 'event': event}

def delete(message, arguments):
    full_name = message.full_name()
    user_id = message.sender_id()

    arguments = convert_dates(arguments, 365)
    start_date, end_date = date_period_to_datetime_objects(arguments)

    # Fetching the data

    events = google_calendar.list_range(start_date, end_date)

    deleted = 0
    undo_queue[user_id] = {'action': 'delete', 'events': []}
    for event in events:
        if event['summary'].lower().strip() == full_name.lower().strip():
            google_calendar.delete_event(event['id'])
            undo_queue[user_id]['events'].append(event)
            deleted += 1

    if deleted == 0:
        message.reply("I didn't delete anything because I couldn't find any PTOs from you between " + readable_format(start_date)  + " to " + readable_format(end_date))
        return

    message.reply(":wastebasket: Done! I deleted " + str(deleted) + " PTOs from you.")
    message.reply("You can tell me to undo this.")

    user_id = message.sender_id()

def undo(message):
    user_id = message.sender_id()
    full_name = message.full_name().lower().strip()

    if user_id not in undo_queue or 'action' not in undo_queue[user_id]:
        message.reply("There's nothing you can undo. You could try to delete or create a PTO instead.")
        return

    to_undo = undo_queue[user_id]
    if to_undo['action'] == 'delete':
        undo_delete(to_undo, message)

    if to_undo['action'] == 'add':
        undo_add(to_undo, message)

    undo_queue.pop(user_id, None)

def undo_delete(to_undo, message):
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

def undo_add(to_undo, message):
    full_name = message.full_name()
    event_to_undo = to_undo['event']
    start_date = parse(event_to_undo['start']['date'])
    end_date = parse(event_to_undo['end']['date'])
    events = google_calendar.list_range(start_date, end_date)

    for event in events:
        if event['summary'] == event_to_undo['summary']:
            google_calendar.delete_event(event['id'])
            message.reply("Undone! I deleted that PTO.")
            message.reply("If I got something wrong when making it, you could try again but phrase it differently.")
            break

def generate_attachment(name, type, description, start, end):
    attachment = {}
    attachment["fallback"] = "Calendar event"
    attachment["title"] = name
    if description:
        attachment["footer"] = description

    if type == "end":
        attachment["text"] = "Returns from PTO"
        attachment["color"] = "#2ECC40"
    elif type == "oneDay":
        attachment["text"] = "On PTO for one day"
        attachment["color"] = "#FF851B"
    elif type == "start":
        attachment["text"] = "Starts PTO until they return on " + readable_format(end)
        attachment["color"] = "#FF4136"
    elif type == "continue":
        attachment["text"] = "Still on PTO from " + readable_format(start) + " until they return on " + readable_format(end)
        attachment["color"] = "#0074D9"
    elif type == "future":
        attachment["text"] = "On PTO from " + readable_format(start) + " until they return on " + readable_format(end)
        attachment["color"] = "#0074D9"

    return attachment


def convert_dates(arguments, dayOffset=None):
    if 'date' in arguments and arguments['date']:
        arguments['date-period'] = date_to_date_period(arguments['date'])

    if dayOffset and 'date-period' in arguments and not arguments['date-period']:
        arguments['date-period'] = date_to_date_period(datetime.now(), dayOffset)

    return arguments

def date_to_date_period(date, dayOffset=1):
    if type(date) == str:
        that_day = parse(date)
    else:
        that_day = date
    return iso_format(that_day) + "/" + iso_format(that_day + timedelta(days=dayOffset))

def date_period_to_datetime_objects(arguments):
    dates = arguments['date-period'].split('/')
    start_date = parse(dates[0])
    end_date = parse(dates[1])
    return start_date, end_date

def iso_format(date):
    return date.strftime('%Y-%m-%d')

def readable_format(date):
    return date.strftime("%A, %d %B")
