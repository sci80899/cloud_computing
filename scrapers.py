from bs4 import BeautifulSoup
import requests
import urllib.request
import pandas as pd

def find_ID(content):
    content_code = urllib.request.quote(content)
    url = 'https://www.imdb.com/find?q='+content_code+'&ref_=nv_sr_sm'
    r = requests.get(url)
    demo = r.text
    soup = BeautifulSoup(demo, "html.parser")
    strings = soup.find_all('tr',class_='findResult odd')[0].find_all('a', href=True)[1]["href"]
    ID = strings[7:-1]
    return ID

def movieinfo(ID):
    url = 'https://www.imdb.com/title/'+ID + '/'
    r = requests.get(url)
    demo = r.text
    soup = BeautifulSoup(demo, "html.parser")
    info = soup.find('div',class_='title_wrapper')
    title = info.find('h1',class_='').get_text()
    a = info.find('div',class_='subtext').get_text().split('\n')
    level = a[1].strip(' ')
    duration = a[3].strip(' ')
    b = soup.find('div',class_='poster').find('img')
    poster = b.get('src')
    c = soup.find('div',class_='plot_summary')
    story = c.find('div',class_='summary_text').get_text().split(' ')
    story = [i for i in story if i != '' and i != '\n']
    story = " ".join(story)
    people = c.find_all('div',class_='credit_summary_item')
    Director = people[0].get_text().split('\n')[2]
    Stars = people[2].get_text().split('\n')[2]
    d = soup.find('div',class_='ratings_wrapper')
    score = d.find('div',class_='ratingValue').get_text().split('\n')[1]

    movieinfo = pd.DataFrame({'ID':ID,'title':title,'level':level,'score':score,'duration':duration,
                              'poster':poster,'story':story,'director':Director,'stars':Stars},index=[0])
    return movieinfo


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
