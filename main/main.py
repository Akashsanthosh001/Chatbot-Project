import re
from sklearn.metrics.pairwise import cosine_similarity
from features import reminders,weather_api, news_api, web_browse
from memory import user_memory
from responses import general
from features.web_browse import site_urls
import joblib
import spacy
from responses.general import handle_unknown
from utils.preprocessing import preprocess
from sentence_transformers import SentenceTransformer
from nlu.sentiment import get_sentiment
from fallback import fallback_color,fallback_name_update,fallback_location

model = SentenceTransformer("all-MiniLM-L6-v2")
nlp = spacy.load("en_core_web_sm")

embeddings = joblib.load("embeddings.pkl")
intent_labels = joblib.load("labels.pkl")

expected_input = None
user_memory.load_memory("memory.json")

common_colors = {
    "red", "blue", "green", "yellow", "purple", "black", "white",
    "orange", "pink", "brown", "gray", "grey", "gold", "silver",
    "maroon", "navy", "teal", "violet", "indigo", "beige", "cyan"
}

while True:
    # user input and cleaning
    user_prompt = input("You: ")
    clean_input,entities = preprocess(user_prompt)
    input_embedding = model.encode(clean_input).reshape(1,-1)

    similarity_scores = cosine_similarity(input_embedding, embeddings)
    best_index = similarity_scores.argmax()
    predicted_intent = intent_labels[best_index]
    sentiment = get_sentiment(user_prompt)

    news_categories = ["technology","sports","health","business","entertainment","science","general"]

    # sentiment and general
    if sentiment == "positive":
        print("Bot: I'm glad to hear that!")
    elif sentiment == "negative":
        print("Bot: I'm here for you. Want to talk about it?")
    elif clean_input in ["bye","exit"]:
        print("Bot:Bye! Have a nice day!!")
        break
    elif clean_input in ["nice" , "good"]:
        general.say_good()
    elif predicted_intent == "greeting":
        general.handle_greeting()
    elif "help" in clean_input:
        general.handle_help()
    elif any(word in clean_input for word in ["thanks","thank you" , "thankyou"]):
        general.handle_thanks(user_prompt)
        break

    # weather
    elif predicted_intent == "weather":
        response = weather_api.handle_weather(user_prompt)
        print(response)

    # joke
    elif predicted_intent == "joke":
        general.handle_joke()

    #news
    elif predicted_intent in news_categories:
        news = news_api.handle_news(predicted_intent,user_prompt)
        print("Bot: ",news)

    # add , show , delete reminders
    elif predicted_intent == "show_reminder":
        reminders.show_reminders()
    elif predicted_intent == "delete_reminder":
        reminders.delete_reminders(clean_input)
    elif predicted_intent == "add_reminder":
        reminders.add_reminders(clean_input,nlp)
    elif clean_input in ["exit","bye"]:
         break

    # entering name for first time and updating the current name
    elif predicted_intent in ["update_name","name_info"]:
        name_fallback = fallback_name_update(user_prompt, entities)
        if name_fallback:
            user_memory.save_user_info("name", name_fallback)
            user_memory.save_memory("memory.json")
            print(f"Bot: Got it! I’ve updated your name to {name_fallback.title()}")
            continue
        elif predicted_intent == "name_info":
            name = entities.get("person")
            if not name:
                match = re.match(r"(?:no my name is|i am|i'm|this is|they call me)\s+([a-zA-Z\s'-]+)", user_prompt,
                                 re.IGNORECASE)
                if match:
                    name = match.group(1).strip()
            elif re.fullmatch(r"[a-zA-Z\s'-]+", name):
                user_memory.save_user_info("name", name)
                user_memory.save_memory(filename="memory.json")
                print(f"Bot: Nice to meet you, {name.title()}")
            else:
                print("Bot: Please provide a valid name!")

    #entering the name
    elif expected_input == "name":
        if user_prompt.isalpha():
            user_memory.save_user_info("name",user_prompt)
            print(user_memory.extract_user_info("name"))
            user_memory.save_memory(filename="memory.json")
        else:
            print("Bot: Please provide a valid name")

    # asking the bot whether it remember the name
    elif predicted_intent == "name_check":
        print(user_memory.double_check_userinfo("name"))

    # giving a new location for first time
    elif predicted_intent == "location":
        if "loc" in entities:
            loc = entities["loc"]
            user_memory.save_user_info("location", loc)
            print(user_memory.extract_user_info("location"))
            user_memory.save_memory(filename="memory.json")
        elif "gpe" in entities:
            loc = entities["gpe"]
            user_memory.save_user_info("location", loc)
            print(user_memory.extract_user_info("location"))
            user_memory.save_memory(filename="memory.json")
        else:
            match = re.search(r"(?:live in|located at|home is in|current location|reside in|settled at)\s([a-zA-Z\s-]+)",user_prompt,re.IGNORECASE)
            if match:
                loc = match.group(2).strip()
                user_memory.save_user_info("location",loc)
                print(user_memory.extract_user_info("location"))
                user_memory.save_memory(filename="memory.json")

    # updating the existing location
    elif predicted_intent == "update_location":
        if "loc" in entities:
            loc = entities["loc"]
            user_memory.save_user_info("location", loc)
            print(user_memory.print_corrected_info("location"))
            user_memory.save_memory(filename="memory.json")
        elif "gpe" in entities:
            loc = entities["gpe"]
            user_memory.save_user_info("location", loc)
            print(user_memory.print_corrected_info("location"))
            user_memory.save_memory(filename="memory.json")
        else:
            location_fallback = fallback_location(user_prompt,entities)
            if location_fallback:
                user_memory.save_user_info("location", location_fallback)
                print(user_memory.print_corrected_info("location"))
                user_memory.save_memory(filename="memory.json")

    # ask bot whether it remember the location
    elif predicted_intent == "check_location":
        print(user_memory.double_check_userinfo("location"))

    # entering favourite color for first time
    elif "color"  in entities and predicted_intent != "update_favorite_color":
        current_color = user_memory.extract_user_info("favourite color")
        new_color = fallback_color(user_prompt, entities, common_colors)
        if new_color and new_color != current_color:
            user_memory.save_user_info("favourite color", new_color)
            print(user_memory.extract_user_info("favourite color"))
            user_memory.save_memory(filename="memory.json")
            continue

    #updating the existing favourite color
    elif predicted_intent == "update_favorite_color":
        existing_color = user_memory.has_info("favourite color")
        if not existing_color:
            print("Bot: I don't know your favorite color yet. Want to tell me?")
        else:
            color = fallback_color(user_prompt, entities, common_colors)
            if color:
                user_memory.save_user_info("favourite color", color)
                print(user_memory.print_corrected_info("favourite color"))
                user_memory.save_memory(filename="memory.json")
            else:
                print("Bot: I don't know your favourite color yet!")

    # checking it remember the favourite color
    elif predicted_intent == "favourite_color":
        print(user_memory.double_check_userinfo("favourite color"))

       # web browse
    elif predicted_intent == "search_web":
        query = user_prompt
        response = web_browse.search_web(query)
        print("Bot:",response)

    #open website
    elif predicted_intent == "open_website":
        site = web_browse.extract_site_name(user_prompt)
        if site and site in site_urls:
            response = f"Here's the link to {site.title()}: {site_urls[site]}"
        else:
            response = "Sorry, I couldn't recognize the website you want to open"
        print("Bot: ",response)

    # extracting all saved info
    elif predicted_intent == "check_user":
        user_memory.show_memory()
    else:
        handle_unknown()