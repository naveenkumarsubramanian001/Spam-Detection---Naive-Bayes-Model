# -*- coding: utf-8 -*-
"""CodeSoft task 4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZbBZrJV0RovAOKTgdoupzidFdS0OTPYW
"""

import numpy as np
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from nltk.tokenize import word_tokenize, sent_tokenize

spam_data = pd.read_csv('/content/spam.csv', encoding='latin-1' )

spam_data.rename(columns={'v1': 'target', 'v2': 'text'}, inplace=True)

spam_data.head()

spam_data.shape

spam_data.isnull().sum()

encoder = LabelEncoder()

spam_data['target'] = encoder.fit_transform(spam_data['target'])

spam_data['target'].value_counts()

def add_text_length_features(df):
    df['num_characters'] = df['text'].apply(len)
    df['num_words'] = df['text'].apply(lambda text: len(word_tokenize(text)))
    df['num_sentences'] = df['text'].apply(lambda text: len(sent_tokenize(text)))
    return df

import nltk
nltk.download('punkt')

spam_data = add_text_length_features(spam_data)

import nltk
nltk.download('stopwords')

spam_data = spam_data.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1)

spam_data.head()

def stemming (content):
  stemmer = PorterStemmer()
  stemmed_content = re.sub('[^a-zA-Z]',' ',content)
  stemmed_content = stemmed_content.lower()
  stemmed_content = stemmed_content.split()
  stemmed_content = [stemmer.stem(word) for word in stemmed_content if not word in stopwords.words('english')]
  stemmed_content = ' '.join(stemmed_content)
  return stemmed_content

spam_data['text'] = spam_data['text'].apply(stemming)

X = spam_data.drop(['target'] , axis = 1)

Y = spam_data['target'].values

X.head()

vectorizer = TfidfVectorizer()

X_text = vectorizer.fit_transform(spam_data['text'])
X_features = spam_data[['num_characters', 'num_words', 'num_sentences']].values
X = np.hstack((X_text.toarray(), X_features))

Y = spam_data['target'].values

X_train , X_test , Y_train , Y_test = train_test_split(X , Y , test_size = 0.2 , stratify = Y)

model = GaussianNB()

model.fit(X_train, Y_train)

train_pred = model.predict(X_train)
test_pred = model.predict(X_test)

score = accuracy_score(Y_train , train_pred)
print(score)
score1 = accuracy_score(Y_test , test_pred)
print(score1)

confusion_matrix(Y_train , train_pred)
