import google.generativeai as genai
import os

# --- IMPORTANT ---
# Paste your NEWLY generated API key here, inside the quotes.
# Do NOT share this file or a screenshot of it.
YOUR_API_KEY = "AIzaSyD_aEIHJqo7NLge8v48pCLKF1o1qCOkN4c"

try:
    genai.configure(api_key=YOUR_API_KEY)
except Exception as e:
    print(f"Error configuring API: {e}")
    exit()

print("--- Finding available models for 'generateContent' ---")
print("-" * 50)

try:
    for model in genai.list_models():
        # Check if the model supports the 'generateContent' method
        if 'generateContent' in model.supported_generation_methods:
            print(f"Model name: {model.name}")
            print(f"  Description: {model.description}")
            print("-" * 50)
except Exception as e:
    print(f"An error occurred while listing models: {e}")

print("--- Search complete ---")