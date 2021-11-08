import random
import json
import pickle
import numpy
import os

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model

wnl = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

model = load_model('chatbot_model.model')

def greet():
    print("Hello!!! How can I help you?")

def clean_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [wnl.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_sentence(sentence)
    bag = [0]*len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return numpy.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(numpy.array([bow]))[0]
    ERROR_TRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r > ERROR_TRESHOLD]

    results.sort(key=lambda x:x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent':classes[r[0]], 'probability': str(r[1])})

    return return_list


def get_response(intents_list,intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['response'])
            break
    return result

os.system('cls')
greet()

while True:
    message = input("")
    ints = predict_class(message)
    res = get_response(ints, intents)
    
    print()
    print(res)
