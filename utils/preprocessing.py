import nltk
import spacy
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))
nlp = spacy.load("en_core_web_sm")

#clean the user input by tokenizing , lemmatizing  and removing stop words
def preprocess(text):
    text = text.strip().lower()
    tokenized_input = nltk.word_tokenize(text)
    lemmatized_input = [lemmatizer.lemmatize(word) for word in tokenized_input]
    filtered_input = [word for word in lemmatized_input if word not in stop_words and re.match(r'\w+', word)]
    clean_input = " ".join(filtered_input)
    doc = nlp(text)
    entities = {}
    for ent in doc.ents:
        entities[ent.label_.lower()] = ent.text

    common_colors = {
        "red", "blue", "green", "yellow", "purple", "black", "white",
        "orange", "pink", "brown", "gray", "grey", "gold", "silver",
        "maroon", "navy", "teal", "violet", "indigo", "beige", "cyan"
    }
    for word in filtered_input:
        if word in common_colors:
            entities["color"] = word
            break

    return clean_input,entities