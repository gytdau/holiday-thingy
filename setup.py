from setuptools import setup

setup(
   name='ptothingy',
   version='1.0',
   description='A Slack bot that integrates with Google Calendar and Api.ai to manage PTOs',
   install_requires=['slackbot', 'schedule', 'httplib2', 'google-api-python-client', 'oauth2client==3.0.0']
)
