import requests
import os
from dotenv import load_dotenv

load_dotenv()

user_name=os.getenv("api_key")

password=os.getenv("api_secret")

def send_message(to: str, message: str) -> None:

    url = 'https://messages-sandbox.nexmo.com/v1/messages'

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    # auth = ('a4467491', 'PDD3kPizdpT8OiLe')

    auth=(user_name,password)
    data = {
        "from": "14157386102",
        "to": to,
        "message_type": "text",
        "text": message,
        "channel": "whatsapp"
    }

    response = requests.post(url, headers=headers, auth=auth, json=data)
    # print(message)
    print(f"Message sent successfully. Response: {response.text}")
    