import random
import json
import pickle
import numpy
import os
import time

import nltk
from nltk.stem import WordNetLemmatizer
from data import *
from tabulate import tabulate

from tensorflow.keras.models import load_model

wnl = WordNetLemmatizer()

# load json file
intents = json.loads(open('intents.json').read())

# load the bytestream 
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

# load training model
model = load_model('chatbot_model.model')

# print greetings
def greet():
    print("Hello!!! How can I help you?")
    print("Order food/Order Status/Cancel Order")

def clean_sentence(sentence):
    # split string into list of substring
    sentence_words = nltk.word_tokenize(sentence)
    # convert word to base form
    sentence_words = [wnl.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    # get list of word in base form
    sentence_words = clean_sentence(sentence)
    # set array elements to 0
    bag = [0]*len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return numpy.array(bag)

def predict_class(sentence):
    # get list of words
    bow = bag_of_words(sentence)

    # calculate probability
    res = model.predict(numpy.array([bow]))[0]
    ERROR_TRESHOLD = 0.25
    # save result if value larger than error treshold
    results = [[i,r] for i,r in enumerate(res) if r > ERROR_TRESHOLD]

    # sort data descending
    results.sort(key=lambda x:x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent':classes[r[0]], 'probability': str(r[1])})

    return return_list

def get_response(intents_list,intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']

    # select response based on tag
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['response'])
            break
    return result

def obtain_method():
    print("You want to pick up or delivery?")
    ans = input("")
    print()

# clear console
os.system('cls')
greet()

while True:
    # keep listening
    message = input("")
    # calculate probability and get intent
    ints = predict_class(message.lower())
    # use intent to get response
    res = get_response(ints, intents)
    
    print()
    
    # Check if display menu needed
    menu = categorize(ints[0]['intent'])


    if (ints[0]['intent']!="delivery"):
        # print response if not check for food with delivery available 
        print(res)
        # greet if end of conversation
        if ((ints[0]['intent']=="Payment method") or (ints[0]['intent']=="Order status for delivery") or (ints[0]['intent']=="Contactless delivery policy") or (ints[0]['intent']=="Order status for pick up") or (ints[0]['intent']=="Cancel order") or (ints[0]['intent']=="recommend") or (ints[0]['intent']=="About us")):
            print()
            time.sleep(1.5)
            print()
            time.sleep(1.5)
            greet()

    # to print table
    if menu:
        temp=[]
        for i in menu:
            temp.append([i[1],float(i[2]),i[3]])

        # convert array to table
        table = tabulate(temp, headers=['Food', 'Price (RM)','Delivery'], tablefmt='orgtbl')
        print(table)
        obtain_method()
        print("Please make your order!!! (specify food name)")
        