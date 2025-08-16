import requests
import os

def send_discord_message(content):
    discord_webhook_url = os.environ.get("DISCORD_WEBHOOK_URL", "")
    if not discord_webhook_url:
        print("No Discord webhook URL set.")
        return
    data = {"content": content}
    try:
        r = requests.post(discord_webhook_url, json=data)
        if r.status_code != 204:
            print(f"Discord webhook error: {r.text}")
        else:
            print("Message sent to Discord.")
    except Exception as e:
        print(f"Failed to send to Discord: {e}")
