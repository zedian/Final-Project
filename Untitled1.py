#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask,request
app = Flask(__name__)

from flask_cors import CORS
CORS(app)
import tensorflow as tf
import keras
import re
import pickle
import json
import numpy as np
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences


# In[2]:


with open('tokenizer.txt','rb') as f:
    tokenizer = pickle.load(f)
f.close()


# In[3]:


import spacy
from spacy.lang.en import English

nlp = spacy.load('en')


# In[4]:


def clean_text(text):
    text = re.sub(r'[^a-zA-Z]+\s+', ' ', text)
    text = text.lower()
    return text


# In[5]:


contraction_dict = {"ain't": "is not", "aren't": "are not","can't": "cannot", "'cause": "because", 
    "could've": "could have", "couldn't": "could not", "didn't": "did not",  "doesn't": "does not", 
    "don't": "do not", "hadn't": "had not", "hasn't": "has not", "haven't": "have not", 
    "he'd": "he would","he'll": "he will", "he's": "he is", "how'd": "how did", "how'd'y": "how do you",
    "how'll": "how will", "how's": "how is",  "I'd": "I would", "I'd've": "I would have", "I'll": "I will",
    "I'll've": "I will have","I'm": "I am", "I've": "I have", "i'd": "i would", "i'd've": "i would have",
    "i'll": "i will",  "i'll've": "i will have","i'm": "i am", "i've": "i have", "isn't": "is not",
    "it'd": "it would", "it'd've": "it would have", "it'll": "it will", "it'll've": "it will have",
    "it's": "it is", "let's": "let us", "ma'am": "madam", "mayn't": "may not", "might've": "might have",
    "mightn't": "might not","mightn't've": "might not have", "must've": "must have", "mustn't": "must not",
    "mustn't've": "must not have", "needn't": "need not", "needn't've": "need not have","o'clock": "of the clock",
    "oughtn't": "ought not", "oughtn't've": "ought not have", "shan't": "shall not", "sha'n't": "shall not", 
    "shan't've": "shall not have", "she'd": "she would", "she'd've": "she would have", "she'll": "she will", 
    "she'll've": "she will have", "she's": "she is", "should've": "should have", "shouldn't": "should not", 
    "shouldn't've": "should not have", "so've": "so have","so's": "so as", "this's": "this is",
    "that'd": "that would", "that'd've": "that would have", "that's": "that is", "there'd": "there would",
    "there'd've": "there would have", "there's": "there is", "here's": "here is","they'd": "they would", 
    "they'd've": "they would have", "they'll": "they will", "they'll've": "they will have", 
    "they're": "they are", "they've": "they have", "to've": "to have", "wasn't": "was not", 
    "we'd": "we would", "we'd've": "we would have", "we'll": "we will", "we'll've": "we will have", 
    "we're": "we are", "we've": "we have", "weren't": "were not", "what'll": "what will", 
    "what'll've": "what will have", "what're": "what are",  "what's": "what is", "what've": "what have", 
    "when's": "when is", "when've": "when have", "where'd": "where did", "where's": "where is", 
    "where've": "where have", "who'll": "who will", "who'll've": "who will have", "who's": "who is", 
    "who've": "who have", "why's": "why is", "why've": "why have", "will've": "will have", "won't": "will not", 
    "won't've": "will not have", "would've": "would have", "wouldn't": "would not", "wouldn't've": "would not have", 
    "y'all": "you all", "y'all'd": "you all would","y'all'd've": "you all would have","y'all're": "you all are",
    "y'all've": "you all have","you'd": "you would", "you'd've": "you would have", "you'll": "you will", 
    "you'll've": "you will have", "you're": "you are", "you've": "you have"}

#Here we use a dictionary of common contractions in order to compile a regex pattern which will be used to replace contractions by their appropriate text
def _get_contractions(contraction_dict):
    contraction_re = re.compile('(%s)' % '|'.join(contraction_dict.keys()))
    return contraction_dict, contraction_re

contractions, contractions_re = _get_contractions(contraction_dict)

def replace_contractions(text):
    def replace(match):
        return contractions[match.group(0)]
    return contractions_re.sub(replace, text)


# In[6]:


import string

stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're",
             "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he',
             'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's",
             'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
             'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was',
             'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did',
             'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
             'while', 'of', 'at', 'by', 'for', 'with', 'about', 'between', 'into',
             'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
             'in', 'out', 'on', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
             'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few',
             'most', 'other', 'some', 'such', 'own', 'same', 'so', 'than',
             'too', 'very', 's', 't', 'can', 'will', 'just', 'should', "should've",
             'now', 'd', 'll', 'm', 'o', 're', 've', 'y']
punctuations = string.punctuation


# In[7]:


def get_tokens(text):
    tokens = nlp(text)
    tokens = [tok.lemma_.lower().strip() for tok in tokens if tok.lemma_ != '-PRON-']
    tokens = [tok for tok in tokens if tok not in stopwords and tok not in punctuations]
    return tokens


# In[8]:


def preprocessing_text(text):
    text = clean_text(text)
    text = replace_contractions(text)
    text = get_tokens(text)
    text = " ".join(text)
    return text


# In[9]:


def create_model():
    global model
    model = load_model('modelCNN.h5')
    model._make_predict_function()


# In[10]:


@app.route('/',methods=['POST'])
def getbinary():
    text = request.form.get('text')
    x = processing_text(text)
    x = tokenizer.texts_to_sequences([x])
    x = pad_sequences(x, maxlen=75)
    sin = model.predict(x)
    binary = np.round(sin)
    return json.dumps(binary)


# In[11]:


if __name__ == "__main__":
    create_model()
    app.run(host='0.0.0.0',port=4222, debug = True)
    


# In[ ]:


get_ipython().run_line_magic('tb', '')


# In[ ]:




