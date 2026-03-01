import requests
import os
from dotenv import load_dotenv

load_dotenv()

INSTANCE_ID = os.getenv("GREEN_API_INSTANCE_ID")
API_TOKEN   = os.getenv("GREEN_API_TOKEN")
GROUP_ID    = os.getenv("GREEN_API_GROUP_ID")

BASE_URL = f"https://api.green-api.com/waInstance{INSTANCE_ID}"


def send_message(text: str) -> bool:
    url = f"{BASE_URL}/sendMessage/{API_TOKEN}"
    payload = {
        "chatId": GROUP_ID,
        "message": text
    }
    response = requests.post(url, json=payload)
    
    if response.status_code != 200:
        print(f"HTTP Error: {response.status_code}")
        print(f"Response body: {response.text}")
        return False
    
    return True


if __name__ == "__main__":
    success = send_message("Testing Green API")
    
    if success:
        print("Success")
    else: 
        print("Something went wrong")