import requests
import spacy
import re

nlp = spacy.load("en_core_web_sm")

from dotenv import load_dotenv
import os
import requests

load_dotenv()
key = os.getenv("NEWS_API_KEY")

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

def handle_news(predicted_intent,user_prompt):
    location = extract_city(user_prompt)

    api_key = "Your api key"

    category_map = {
        "technology": "technology",
        "sports": "sports",
        "health": "health",
        "business": "business",
        "entertainment": "entertainment",
        "science": "science",
        "general": "general"
    }

    category = category_map.get(predicted_intent, "general")

    if location:
        query = f"{location} {category}" if category else location
        url = f"https://newsapi.org/v2/everything?q={query}&language=en&pageSize=5&apiKey={api_key}"
    else:
        url = f"https://newsapi.org/v2/top-headlines?category={category}&language=en&pageSize=5&apiKey={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors

        news_data = response.json()
        articles = news_data.get("articles", [])

        if not articles:
            return "Sorry, I couldn't find any news articles right now."

        headlines = [f"{i+1}. {article['title']}" for i, article in enumerate(articles[:5])]
        return "\n".join(headlines)

    except requests.exceptions.RequestException as e:
        return f"An error occurred while fetching news: {str(e)}"
    except Exception:
        return "Something went wrong while processing the news."
