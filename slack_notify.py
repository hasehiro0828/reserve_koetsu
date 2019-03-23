import requests

import config

SLACK_TOKEN = config.SLACK_TOKEN
SLACK_ID = config.SLACK_ID


def notify(message, screenshot_filename):
    files = {'file': open(screenshot_filename, 'rb')}
    param = {
        'token': SLACK_TOKEN,
        'channels': SLACK_ID,
        'filename':screenshot_filename,
        'content':message,
        'initial_comment':message
    }

    requests.post(url="https://slack.com/api/files.upload", params=param, files=files)

def send_message(message):
    param = {
        'token': SLACK_TOKEN,
        'channel': SLACK_ID,
        'text': message,
    }
    requests.post(url="https://slack.com/api/chat.postMessage", params=param)