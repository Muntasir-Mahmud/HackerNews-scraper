import requests
import json

from celery import Celery
from bs4 import BeautifulSoup
from datetime import datetime
from celery.schedules import crontab


app = Celery('tasks')

app.conf.timezone = 'UTC'

app.conf.beat_schedule = {
    'scraping-task-one-minute': {
        'task': 'tasks.hackernews_rss',
        'schedule': crontab(),
    }
}


@app.task
def save_function(article_list):
    '''Save the results of scraping'''
    timestamp = datetime.now().strftime('%d%m%Y, %H%M%S')

    filename = 'articles-{}.json' .format(timestamp)
    with open(filename, 'w') as outfile:
        json.dump(article_list, outfile, indent=4)


@app.task
def hackernews_rss():
    '''Main scraping function'''
    article_list = []

    try:
        r = requests.get('https://news.ycombinator.com/rss')
        soup = BeautifulSoup(r.content, features='xml')
        articles = soup.find_all('item')

        for a in articles:
            title = a.find('title').text
            link = a.find('link').text
            published = a.find('pubDate').text

            article = {
                'title': title,
                'link': link,
                'published': published,
                'created_at': str(datetime.now()),
                'source': 'HackerNews RSS'
            }
            article_list.append(article)

        return save_function(article_list)

    except Exception as e:
        print('The Scraping job failed. See exception: ')
        print(e)
