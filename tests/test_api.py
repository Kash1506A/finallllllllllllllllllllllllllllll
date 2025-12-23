import os
import requests

# Set your API key
API_KEY = "hf_xxxxxxxxxxxxx"
MODEL = "meta-llama/Meta-Llama-3-8B-Instruct"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

payload = {
    "inputs": "Generate a JSON plan for video editing: remove filler words and add subtitles",
    "parameters": {
        "max_new_tokens": 200,
        "temperature": 0.7
    }
}

response = requests.post(
    f"https://api-inference.huggingface.co/models/{MODEL}",
    headers=headers,
    json=payload
)

print(response.json())