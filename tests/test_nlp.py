
import mock, pytest, requests
from pytest_mock import mocker
from holiday_bot import nlp, slackbot_settings

def test_attempts_request(mocker):
    mocker.patch('requests.get')
    nlp.query(3, 'Text to parse...')
    requests.get.assert_called_once_with('https://api.api.ai/api/query', headers={'Authorization': 'Bearer ' + slackbot_settings.API_AI_KEY}, params={'v': 20150910, 'query': 'Text to parse...', 'lang': 'en', 'sessionId': 3})
