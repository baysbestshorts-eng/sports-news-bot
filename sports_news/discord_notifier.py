import requests
import os

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "")

def send_discord_message(content):
    if not DISCORD_WEBHOOK_URL:
        print("No Discord webhook URL set.")
        return
    data = {"content": content}
    try:
        r = requests.post(DISCORD_WEBHOOK_URL, json=data)
        if r.status_code != 204:
            print(f"Discord webhook error: {r.text}")
        else:
            print("Message sent to Discord.")
    except Exception as e:
        print(f"Failed to send to Discord: {e}")
