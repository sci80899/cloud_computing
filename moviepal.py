import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import urllib.request
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing import sequence


def to_numbers(word):
    number = []
    index_from = 3
    word_to_id = imdb.get_word_index()
    word_to_id = {k: (v + index_from) for k, v in word_to_id.items()}
    word_to_id['<PAD>'] = 0
    word_to_id['<START>'] = 1
    word_to_id['<UNK>'] = 2
    word_to_id['<UNUSED>'] = 3
    p = '1234567890[!"#$%&()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+\n'
    l = ""
    for char in word.lower():
        if char not in p:
            l = l + char
    word_new = l.strip('\n').split(' ')
    for id in word_new:
        if id in word_to_id.keys():
            a = word_to_id[id]
            if a <=20000:
                number.append(a)
            else:
                number.append(2)
        else:
            number.append(2)
    return number

def review_scraper(ID):
    url = 'https://www.imdb.com/title/' + ID + '/reviews?filter=prolific'
    r = requests.get(url)
    demo = r.text
    soup = BeautifulSoup(demo, "html.parser")
    users = []
    ratings = []
    movie_reviews = []
    all_containers = soup.find_all('div', class_='review-container')

    i = 1
    for container in all_containers:
        user_tag = container.find("span", {"class": "display-name-link"})
        rating_tag = container.find("span", {"class": "rating-other-user-rating"})
        review_tag = container.find('div', {'class': 'text show-more__control'})
        if not rating_tag or not review_tag or not user_tag:
            continue
        user_text = user_tag.text.strip()
        rating = rating_tag.findChildren('span')[0].text.strip()
        review_text = review_tag.text.strip()
        users.append(user_text)
        ratings.append(rating)
        movie_reviews.append(review_text)
        i = i + 1
        if i > 10:
            break

    all_reviews = pd.DataFrame({'user name': users, 'score': ratings, 'review': movie_reviews, })
    return all_reviews


def moviepal(ID):
    review_model = Sequential()
    review_model.add(Embedding(20000, 128))
    review_model.add(LSTM(128, return_sequences=True))
    review_model.add(LSTM(64, return_sequences=False))
    review_model.add(Dense(1, activation='sigmoid'))
    review_model.compile(loss='binary_crossentropy',optimizer=Adam(0.001),metrics=['accuracy'],)
    review_model.load_weights('imdb_lstm.h5')
    review = review_scraper(ID)
    x = []
    for i in range(len(review['review'])):
        #b = sequence.pad_sequences([to_numbers(review['review'][i])], maxlen=100)
        x.append(to_numbers(review['review'][i]))
    x = sequence.pad_sequences(x, maxlen=100)
    sentiment = review_model.predict(x)
    score = pd.to_numeric(review['score']).round(0).astype(float)
    review['sentiment'] = sentiment
    review['sort'] = score * review['sentiment']
    review.sort_values(by = 'sort',ascending = False, inplace=True)
    review.reset_index(drop=True, inplace=True)
    return review.head(3)

