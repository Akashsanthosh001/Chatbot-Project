import random

#greeting
def handle_greeting():
    responses = [
        "Bot: Hey there!",
        "Bot: Hello! How can I help you today?",
        "Bot: Hi! Ready when you are.",
        "Bot: Hey! What can I do for you?",
        "Bot: Nice to see you! What’s up?"
    ]
    print(random.choice(responses))

#affection
def respond_to_affection(user_prompt):
    responses = {
        "how are you": ["I’m doing great! Thanks for asking 😊", "Feeling fantastic today! You?"],
        "i love you": ["Aww, that’s sweet ❤️", "You’re making me blush 😄", "I love you too — in a bot kind of way!"]
    }

    for key, value in responses.items():
        if key in user_prompt.lower():
            print(random.choice(value))
            return True
    return False

#help queries
def handle_help():
    print("Bot: Sure, I can assist you!")

#thanks
def handle_thanks(user_prompt):
    thanks = {"thank you": ["Anytime! 😊", "Glad I could help!", "You're always welcome!"]}
    for key, value in thanks.items():
        if key in user_prompt.lower():
            print(random.choice(value))
            return True
    return False

def say_good():
    print("Bot: it was nice to hear from you! How can i help you?")

#jokes
def handle_joke():
    jokes = ["Why don’t skeletons fight each other? They don’t have the guts.",
             "Why did the scarecrow win an award? Because he was outstanding in his field!",
             "I told my wife she was drawing her eyebrows too high. She looked surprised.",
             "Why don’t eggs tell jokes? They’d crack each other up!"]

    selected_joke = random.choice(jokes)
    print(f"Bot: {selected_joke}")

#fallback
def handle_unknown():
    statements = ["Hmm, I’m not sure I got that. Want to try again?",
        "Can you tell me that another way?",
        "Oops, didn’t catch that! Maybe rephrase?",
        "Interesting… but I didn’t quite get it."]

    selected_statements = random.choice(statements)
    print(f"Bot: {selected_statements}")