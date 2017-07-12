import mock, pytest, requests, datetime
from pytest_mock import mocker
from holiday_bot import run
from holiday_bot import commands
from dateutil.parser import parse
from datetime import datetime, timedelta

def test_conversion_of_date_into_date_period():
    assert commands.date_to_date_period("2017-05-03", 2) == "2017-05-03/2017-05-05"

def test_conversion_of_date_into_date_period_with_one_day():
    assert commands.date_to_date_period("2017-05-03") == "2017-05-03/2017-05-04"

def test_convert_dates_from_arguments():
    arguments = {
        'date': '2017-05-03'
    }
    assert commands.convert_dates(arguments)['date-period'] == "2017-05-03/2017-05-04"

def test_convert_dates_from_arguments_does_nothing():
    arguments = {
        'date-period': '2017-05-03/2017-05-06'
    }
    assert commands.convert_dates(arguments, 7)['date-period'] == '2017-05-03/2017-05-06'

def test_convert_date_periods_to_datetime_objects():
    arguments = {
        'date-period': '2017-05-03/2017-05-06'
    }
    start, end = commands.date_period_to_datetime_objects(arguments)
    assert start.strftime('%Y-%m-%d') == "2017-05-03"
    assert end.strftime('%Y-%m-%d') == "2017-05-06"

def test_attachment_generation():
    result = commands.generate_attachment("John Doe", "future", "Description...", datetime.now(), datetime.now() + timedelta(days=3))
    assert result["footer"] == "Description..."
    assert result["title"] == "John Doe"

def test_iso_format():
    assert commands.iso_format(parse("2017-01-01")) == "2017-01-01"

def test_readable_format():
    assert commands.readable_format(parse("2017-01-01")) == "Sunday, 01 January"
