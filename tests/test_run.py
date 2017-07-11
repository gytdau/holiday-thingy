# Allow modules to be imported from parent directory
import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import run, mock, pytest, requests, commands
from pytest_mock import mocker

def test_execute_list_intent(mocker):
    mocker.patch('commands.list')
    run.execute_intent("list", 1, 2)
    commands.list.assert_called_once_with(1, 2)

def test_undo_intent(mocker):
    mocker.patch('commands.undo')
    run.execute_intent("undo", 1, 2)
    commands.undo.assert_called_once_with(1)
