import os
import json
import requests

def send_message(message, webhook_url=None, debug=False):
    if not webhook_url:
        webhook_url = os.getenv("TRADES_SLACK_HOOK")
        if debug:
            webhook_url = os.getenv("TRADES_SLACK_HOOK_DEBUG")
        if not webhook_url:
            return None

    slack_data = {"text": message}

    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )

    return True