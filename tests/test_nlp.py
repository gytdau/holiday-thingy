# Allow modules to be imported from parent directory
import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import nlp
import mock
import pytest
from pytest_mock import mocker
import requests

def test_attempts_request(mocker):
    mocker.patch('requests.get')
    nlp.query(3, 'Text to parse...')
    requests.get.assert_called_once()
