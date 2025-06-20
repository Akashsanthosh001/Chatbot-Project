import joblib
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

training_sentences = ["what's my name","do you know my name","can you tell me my name","you remember who I am",
    "do you remember my name","tell me who I am","do you know who i am","can you remember my name",
    "my name is Akash","you can call me Raj","I am Manoj","just call me Sarah",
    "I'm Alice","the name is David",
    "no,my name is akash","actually my name is hari","let me correct that,i'm gokul","can you update my name to akash","sorry,my actual name is daniel",
    "actually i update my name to arjun","actually it's john","actually my name is smith","not akash,it's hari","sorry, my name is amit","no actually my name is akash",
    "I said my name is Gokul","wait, it's actually Manoj","actually my name is not Akash, it’s Hari","no, you got it wrong, I’m Gokul","let me correct that, my name is Hari",
    "my real name is Gokul","correction, my name is Gokul","oh, I meant to say my name is Manoj","no no no no no no no",
    "hello","hi there","hey","good morning","good evening","what's up","how are you",
    "how's it going","yo","hi buddy",
    "tell me a joke","make me laugh","say something funny","give me a joke",
    "I want to hear a joke","can you joke with me",
    "I want to change my favorite color to blue.","Make red my new favorite color.","Replace my current favorite color with yellow.",
    "Change it to purple.","I want to change my favorite color to pink","Set my color preference to orange.",
    "I no longer like blue; change my favorite color to pink.","Update it to black please","Now I like teal",
    "what's my favorite color", "do you remember my favorite color",
    "can you tell me my favorite colour","do you know what color I like",
    "what colour do I like","tell me my favorite color",
    "my favourite color is blue" , "i like the color red","red is my favourite color",
    "most favourite color is orange","I really love orange","Definitely navy blue","It's beige","I like indigo",
    "Remind me to call mom at 6 PM.","Set a reminder for my meeting tomorrow.","Add a reminder to water the plants.","Can you remind me to take my medicine at 8?",
    "I need a reminder for my appointment.","Create a reminder to pay the bills.","Remind me about my homework later.",
    "Set a reminder to go for a walk at 7.","Please remind me to send the email.","I want to add a new reminder.",
    "show me my reminders","what are my reminders","do I have any reminders",
    "list my reminders","reminders list please","tell me my reminders",
    "delete my reminder","remove the reminder","clear the reminder","can you delete reminder","erase the reminder",
    "cancel the reminder I set",
    "i live in haryana" ,"my current location is at kerala","i reside in bengaluru",
    "I'm settled in Lucknow","I'm located in Chandigarh","I'm now in Noida","I'm staying in Thiruvananthapuram",
    "I live in Ranchi","I currently reside in Guwahati","My home is in Visakhapatnam",
    "what's my location","where am I","can you tell my current location",
    "do you know where I am","tell me where I am","my location please","actually i live in chennai",
    "I have relocated to Hyderabad","I recently moved to Chennai","My new location is Ahmedabad",
    "I moved to Jaipur last week","no i live in mumbai","no you are wrong! i live in pune" ,
    "what's the weather like in chennai","tell me the weather in mumbai",
    "how's the weather today at kannur","weather forecast of delhi please","is it raining today at noida","will it be sunny tomorrow at pune",
    "do I need an umbrella in kochi","temperature right now at hyderabad","what's the weather in Delhi","show me today's weather in bangalore",
    "what do you know about me" ,"show my info","list saved details","What user info is stored?","Check my profile details",
    " Read out my saved info","What have I shared with you so far?","Display my personal data",
    "Do you remember my info?",
    "Show me the latest tech news","Any updates in technology?","What’s trending in AI?","Tell me some technology news",
    "Give me current tech updates","Technology headlines today","What's new in gadgets?","Latest in the tech world",
    "Give me sports news","Show me today's sports highlights","Any cricket updates?","What's happening in football?","Sports news please","Did any team win recently?",
    "Latest updates in sports","Tell me about the match results",
    "Show me health news","Latest in healthcare?","Any updates in medical research?","Health headlines today",
    "News on disease outbreaks","Healthcare news please","What's new in medicine?","Health-related news now",
    "Business news please","Any stock market updates?","Show me financial news","What's new in the business world?",
    "Business headlines today","Economic news now","Corporate updates please","Latest business insights",
    "Entertainment news please","can you give some entertainment news please","Any movie releases?","What’s new in Hollywood?","Celebrity news updates",
    "Tell me about the latest shows","TV and film news","Showbiz news today","Who won an award recently?",
    "Give me science news","What are the latest scientific discoveries?","Show me space news","Updates in climate research?",
    "New scientific breakthroughs?","Science headlines please","What's new in research?","Tell me science-related news",
    "Show me top headlines","What's happening around the world?","Any major news today?","Tell me global news","World news right now",
    "What's the breaking news?","General news updates","Top stories please"
                      ]

training_labels = ["name_check", "name_check", "name_check", "name_check", "name_check", "name_check","name_check","name_check",
                   "name_info", "name_info", "name_info", "name_info", "name_info", "name_info",
                   "update_name","update_name","update_name","update_name","update_name","update_name","update_name","update_name","update_name","update_name","update_name",
                   "update_name","update_name","update_name","update_name","update_name","update_name","update_name","update_name","update_name",
                   "greeting", "greeting", "greeting", "greeting", "greeting", "greeting", "greeting", "greeting", "greeting", "greeting",
                   "joke","joke","joke","joke","joke","joke",
                   "update_favorite_color", "update_favorite_color", "update_favorite_color", "update_favorite_color",
                   "update_favorite_color", "update_favorite_color", "update_favorite_color", "update_favorite_color","update_favorite_color",
                   "favourite_color", "favourite_color", "favourite_color", "favourite_color", "favourite_color", "favourite_color",
                   "color_info", "color_info", "color_info", "color_info","color_info", "color_info", "color_info", "color_info",
                   "add_reminder","add_reminder","add_reminder","add_reminder","add_reminder","add_reminder","add_reminder","add_reminder",
                   "add_reminder","add_reminder",
                   "show_reminder", "show_reminder", "show_reminder", "show_reminder", "show_reminder", "show_reminder",
                   "delete_reminder", "delete_reminder", "delete_reminder", "delete_reminder", "delete_reminder", "delete_reminder",
                   "location","location","location","location","location","location","location","location","location","location",
                   "check_location", "check_location", "check_location", "check_location", "check_location", "check_location",
                   "update_location","update_location","update_location","update_location","update_location","update_location","update_location",
                   "weather","weather","weather","weather","weather","weather","weather","weather","weather","weather",
                   "check_user","check_user","check_user","check_user","check_user","check_user","check_user","check_user","check_user",
                   "technology", "technology", "technology", "technology", "technology", "technology", "technology", "technology",
                   "sports", "sports", "sports", "sports", "sports", "sports", "sports", "sports",
                   "health", "health", "health", "health", "health", "health", "health", "health",
                   "business", "business", "business", "business", "business", "business", "business", "business",
                   "entertainment", "entertainment", "entertainment", "entertainment", "entertainment", "entertainment",
                   "entertainment", "entertainment","entertainment",
                   "science", "science", "science", "science", "science", "science", "science", "science",
                   "general", "general", "general", "general", "general", "general", "general", "general"
                   ]

sentence_embeddings = model.encode(training_sentences)

from sklearn.linear_model import LogisticRegression

classifier = LogisticRegression()
classifier.fit(sentence_embeddings , training_labels)

joblib.dump(sentence_embeddings, "embeddings.pkl")          # Saves the trained model
joblib.dump(training_labels, "labels.pkl")

