import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if api_key:
    print(f"Key length: {len(api_key)}")
    print(f"Key repr: {repr(api_key)}")
    print(f"First 20 chars: {api_key[:20]}")
    print(f"Last 20 chars: {api_key[-20:]}")

url = "https://api.groq.com/openai/v1/models"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
print("\nResponse:", response.json())