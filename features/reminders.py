reminders = []
from dateparser import parse as parse_date
import re
import spacy
from fuzzywuzzy import fuzz
import random

nlp = spacy.load("en_core_web_sm")

user_context={"reminder_in_progress":{
    "description":None,
    "time":None
   }
}

def extract_time(user_prompt,nlp):

    doc = nlp(user_prompt)
    for ent in doc.ents:
        if ent.label_.lower() in ["time", "date"]:
            return ent.text

    parsed_time = parse_date(user_prompt)
    if parsed_time:
        return parsed_time.strftime("%I:%M %p on %B %d, %Y")

    return None

def clean_description(user_prompt, time_entity):
    description = user_prompt.replace(time_entity, "") if time_entity else user_prompt

    parsed_time = parse_date(user_prompt)
    if parsed_time:
        # Generate possible time string formats to remove (flexible)
        time_formats = [
            parsed_time.strftime("%I:%M %p").lstrip("0"),
            parsed_time.strftime("%I %p").lstrip("0"),
            parsed_time.strftime("%H:%M"),
            parsed_time.strftime("%B %d"),
            parsed_time.strftime("%d %B"),
            parsed_time.strftime("%A"),
        ]
        for tf in time_formats:
            description = description.replace(tf, "")

    fillers = ["add","remind me to", "reminder", "remind me", "remind", "please", "about", "set",
               "to", "on", "at", "me", "create", "I should", "I have", "I need to","that"]
    for phrase in fillers:
        description = re.sub(rf"\b{phrase}\b", "", description, flags=re.IGNORECASE)

    description = re.sub(r"\s+", " ", description).strip()

    doc = nlp(description)
    for token in doc:
        if token.lemma_ in {"remind", "add", "set", "make", "create"} and token.dep_ == "ROOT":
            for child in token.children:
                if child.dep_ in {"xcomp", "dobj", "prep", "ccomp", "acl", "advcl"}:
                    extracted = doc[child.left_edge.i : child.right_edge.i+1].text.strip()
                    if extracted.lower().startswith(("a ", "an ")):
                        extracted = " ".join(extracted.split(" ")[1:])
                    if extracted.lower() not in {"me", "reminder", "remind"}:
                        return extracted

    if description.lower() in {"me","reminder",""}:
        return None

    return description

def add_reminders(user_prompt,nlp):
    global user_context

    success_response = [
        "Bot: Got it! I've set a reminder for '{description}' at {time}.",
        "Bot: Your reminder for '{description}' at {time} has been saved!",
        "Bot: Reminder noted: '{description}' at {time}.",
        "Bot: I've scheduled: '{description}' at {time}.",
        "Bot: Done! I’ll remind you about '{description}' at {time}."
    ]

    failure_responses = [
        "Bot: Oops! Something was missing. Please mention what and when.",
        "Bot: Hmm, I didn’t catch that. Can you include the time and task?",
        "Bot: Sorry, I need both the task and the time to set a reminder."
    ]

    time_entity = extract_time(user_prompt, nlp)
    description = clean_description(user_prompt, time_entity)

    ctx = user_context["reminder_in_progress"]

    if time_entity:
        ctx["time"] = time_entity
    if description:
        ctx["description"] = description

    if ctx["description"] and ctx["time"]:
        reminders.append({"description":ctx["description"],
                          "time":ctx["time"]})

        response = random.choice(success_response).format(description=ctx["description"],time=ctx["time"])
        print(response)
        ctx["description"] = None
        ctx["time"] = None
    else:
        if not ctx["description"]:
            print(random.choice(failure_responses))
        if not ctx["time"]:
            print(random.choice(failure_responses))

def show_reminders():
    if reminders:
        print("reminders:")
        for reminder in reminders:
            print(f"-{reminder['description']} at {reminder['time']}")
    else:
        print("Bot: You have no reminders!")

def delete_reminders(user_prompt):
    if not reminders:
        print("Bot: You have no reminders to delete.")
        return

    matches = []
    for reminder in reminders:
        description_score = fuzz.partial_ratio(user_prompt.lower(), reminder["description"].lower())
        time_score = fuzz.partial_ratio(user_prompt.lower(), reminder["time"].lower())
        average_score = (description_score + time_score) / 2

        if average_score > 60:
            matches.append((reminder, average_score))

    if not matches:
        print("Bot: I couldn't find any reminder that closely matches your input.")
        return

    # Sort by score, show the best match
    matches.sort(key=lambda x: x[1], reverse=True)
    best_match = matches[0][0]

    print(f"Bot: Did you mean to delete -> '{best_match['description']}' at '{best_match['time']}'? (yes/no)")
    confirm = input("You: ").strip().lower()

    if confirm in ["yes", "y"]:
        reminders.remove(best_match)
        print("Reminder deleted.")
    else:
        print("Deletion cancelled.")

def prompt_delete_reminder():
    if not reminders:
        print("You have no reminders to delete")
        return

    prompt_description = input("Please enter the description: ")
    prompt_time = input("Please enter the time of description: ")

    match_index = -1
    for i,reminder in enumerate(reminders):
        desc_match = reminder.get("description","").lower() == prompt_description.lower()
        time_match = reminder.get("time","").lower() == prompt_time.lower()
        if desc_match and time_match:
            match_index = i
            break

    if match_index != -1:
        deleted = reminders.pop(match_index)
        print(f"Bot: Deleted reminder:{deleted}")
    else:
        print("Bot: No matching reminder found")

