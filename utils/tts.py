import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()
API_KEY = os.getenv("DG_API_KEY")
AUDIO_FILE=r"C:\Users\Naresh Kumar Lahajal\Desktop\FINAL\media\ouput_file.mp3"

def text_to_speech(llm_response):
    # Define the API endpoint
    url = "https://api.deepgram.com/v1/speak?model=aura-asteria-en"

    # Define the headers
    headers = {
        "Authorization": f"Token {API_KEY}",
        "Content-Type": "application/json"
    }

    # Define the payload
    payload = {
        "text": llm_response
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the response content to a file
        with open(AUDIO_FILE, "wb") as f:
            f.write(response.content)
        print("File saved successfully.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Example usage
#transcribed_text = "Hello, how can I help you today?"
#tts(transcribed_text)
