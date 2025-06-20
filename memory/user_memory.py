import json
user_memory = {}

# fallback
def unfinished():
    global expected_input
    expected_input = "name"
    print("Bot: I didn't catch your name.Could you repeat it?")

#save value for the related key
def save_user_info(key, value):
    user_memory[key] = value

# returning the statement for the key saved in file
def extract_user_info(key):
    if key in user_memory:
        if key == "name":
            return f"Bot: Hello {user_memory[key]}! How you feeling today??"
        elif key == "location":
            return f"Bot: Great! {user_memory[key]} is a good place!!"
        elif key == "favourite color":
            return f"Bot: Nice!!Your favourite color is {user_memory[key]}"
    else:
        return f"Bot: I don't know your {key} yet.Could you tell me?"

#returning statement for checking the info
def double_check_userinfo(key):
    if key in user_memory:
        if key == "name":
            return f"Bot: I know your name! Your name is {user_memory[key]}"
        elif key == "location":
            return f"Bot: You already told about the place where you live! You live in {user_memory[key]}!"
        elif key == "favourite color":
            return f"Bot: I knew it! Your favourite color is {user_memory[key]}"
    else:
        return f"Bot: I don't know your {key} yet.Could you tell me?"

#return statement for updating value
def print_corrected_info(key):
    if key in user_memory:
        value = user_memory[key]
        if key == "name":
            return f"Bot: Got it! I've updated your name to {user_memory[key]}"
        elif key == "location":
            return f"Bot: Sure! You location is updated to {user_memory[key]}!"
        elif key == "favourite color":
            return f"Bot: Thank you for correcting! Your favourite color is {user_memory[key]}"
        else:
            return f"Bot: I've updated your {key} to {value}"
    else:
        return f"Bot: I don't know your {key} yet.Could you tell me?"

#saving the data into json file
def save_memory(filename="memory.json"):
    with open(filename, "w") as f:
        json.dump(user_memory, f)

#loading data from file
def load_memory(filename="memory.json"):
    global user_memory
    try:
        with open(filename, "r") as f:
            user_memory = json.load(f)
    except FileNotFoundError:
        user_memory = {}

#print all details in the json file
def show_memory():
    if not user_memory:
        print("Bot: You have no information to print!!")
    else:
        print("Bot: Here's what i know about you")
        for key, value in user_memory.items():
            print(f" - Your {key} is {value}")

#returning key
def has_info(key):
    return key in user_memory