import random
import json
import pickle
import numpy

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

wnl = WordNetLemmatizer()

# read json file
intents = json.loads(open('intents.json').read())

words = []
classes = []
documents = []
# ignore these characters
ignored_letter = ['?','!',',','.']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        # split string in json patterns into list of substring
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        # make list of tuple 
        documents.append((word_list,intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# convert word to base form if word not ignored characters
words = [wnl.lemmatize(word) for word in words if word not in ignored_letter]
words = sorted(set(words))
classes = sorted(set(classes))

# save data in binary
word_file =  open('words.pkl','wb')
pickle.dump(words,word_file)
class_file =  open('classes.pkl','wb')
pickle.dump(classes,class_file)


training = []

# create list with element of 0
output_empty = [0]*len(classes)

for document in documents:
    bag = []
    word_pattern = document[0]
    # convert word to base form
    word_pattern = [wnl.lemmatize(word.lower()) for word in word_pattern]
    for word in words:
        # check word occur in pattern if yes, append 1, if no append 0
        if word in word_pattern:
            bag.append(1)
        else:
            bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag,output_row])

# neural network training
random.shuffle(training)
training = numpy.array(training)

train_x = list(training[:,0])
train_y = list(training[:,1])

model = Sequential()
model.add(Dense(128,input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))

model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
model.fit(numpy.array(train_x), numpy.array(train_y), epochs=200, batch_size=5, verbose=1)
# save training model
model.save("chatbot_model.model")
print("done")