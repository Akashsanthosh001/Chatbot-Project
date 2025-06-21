import requests
import spacy
import re

nlp = spacy.load("en_core_web_sm")

from dotenv import load_dotenv
import os
import requests

load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")


def extract_city(user_prompt):
    doc = nlp(user_prompt.title())
    for ent in doc.ents:
        if ent.label_ == "GPE":
            return ent.text.title()

    # Fallback: use regex to extract word after "at" or "in"
    match = re.search(r'\b(?:at|in|for)\s+([a-zA-Z\s]+)', user_prompt)
    if match:
        raw_city = match.group(1).strip().title()
        clean_city = re.sub(r'\b(right now|today|currently|tomorrow)\b', '', raw_city, flags=re.IGNORECASE)
        return clean_city.strip().title()

    return None

def handle_weather(user_prompt):
    city = extract_city(user_prompt)

    if not city:
        return "I couldn't find a city in your message. Please mention a city name."

    api_key = "Your api key"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data["cod"] == 200:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            return f"Bot: The weather in {city} is {desc} with a temperature of {temp}°C and humidity of {humidity}%."
        else:
            return f"Sorry, I couldn't find weather information for {city}."

    except requests.exceptions.HTTPError as http_error:
        match response.status_code:
            case 400:
                return "Bad request:\n Please check your input"
            case 401:
                return "Unauthorized:\nInvalid API key"
            case 403:
                return "forbidden:\nAccess is denied"
            case 404:
                return "Not Found:\nCity not found"
            case 500:
                return "Internal Server Error:\nPlease try again later"
            case 502:
                return "Bad Gateway:\nInvalid response from the server"
            case 503:
                return "Service Unavailable:\nServer is down"
            case 504:
                return "GateWay Timeout:\nNo response from the server"
            case _:
                return f"HTTP error occured:\n{http_error}"

    except requests.exceptions.ConnectionError:
        return "Connection Error:\nCheck your internet connection"
    except requests.exceptions.Timeout:
        return "Timeout Error:\nThe request timed out"
    except requests.exceptions.TooManyRedirects:
        return "Too many redirects:\nCheck the URL"
    except requests.exceptions.RequestException as req_error:
        return f"Request Error:\n{req_error}"