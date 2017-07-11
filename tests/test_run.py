import mock, pytest, requests
from pytest_mock import mocker
from holiday_bot import run
from holiday_bot import commands

def test_execute_list_intent(mocker):
    mocker.patch('holiday_bot.commands.list')
    run.execute_intent("list", 1, 2)
    commands.list.assert_called_once_with(1, 2)

def test_undo_intent(mocker):
    mocker.patch('holiday_bot.commands.undo')
    run.execute_intent("undo", 1, 2)
    commands.undo.assert_called_once_with(1)
