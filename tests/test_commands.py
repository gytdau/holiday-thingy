import mock, pytest, requests, datetime
from pytest_mock import mocker
from holiday_bot import run
from holiday_bot import commands
from dateutil.parser import parse

def test_conversion_of_date_into_date_period():
    assert commands.date_to_date_period("2017-05-03", 2) == "2017-05-03/2017-05-05"

def test_conversion_of_date_into_date_period_with_one_day():
    assert commands.date_to_date_period("2017-05-03") == "2017-05-03/2017-05-04"

def test_convert_dates_from_arguments():
    arguments = {
        'date': '2017-05-03'
    }
    assert commands.convert_dates(arguments)['date-period'] == "2017-05-03/2017-05-04"

def test_convert_dates_from_arguments_does_nothing(monkeypatch):
    arguments = {
        'date-period': '2017-05-03/2017-05-06'
    }
    assert commands.convert_dates(arguments, 7)['date-period'] == '2017-05-03/2017-05-06'
