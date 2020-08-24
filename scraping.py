import requests
import json
from bs4 import BeautifulSoup


URL = 'https://news.ycombinator.com/rss'


def hackernews_rss():
    article_list = []

    try:
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, features='xml')
        articles = soup.find_all('item')

        for a in articles:
            title = a.find('title').text
            link = a.find('link').text
            published = a.find('pubDate').text

            article = {
                'title': title,
                'link': link,
                'published': published
            }
            article_list.append(article)

        return save_function(article_list)

    except Exception as e:
        print('The Scraping job failed. See exception: ')
        print(e)


def save_function(article_list):
    with open('articles.txt', 'w') as outfile:
        json.dump(article_list, outfile, indent=4)


print('Starting scraping')
hackernews_rss()
print('Finished scraping')
