"""Script to scrape property news from Straitstimes Property Section"""

import re
import sys

import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
STRAITSTIME_WEBSITE_URL = 'http://www.straitstimes.com'


def scrape_article(href):
    page = requests.get(href, headers=HEADERS)

    if page.status_code != 200:
        return None

    # article to return
    article = ''
    photo_url = None
    img_tag = None

    # main photo url
    soup = BeautifulSoup(page.content, 'html.parser')
    photos = soup.find_all('div', class_='media-entity')
    for photo in photos:
        photo_url = photo['resource']   # get the first photo

    if photo_url is not None:
        img_tag = '<img src=\'{0}\' alt=\'Article image\'>'.format(photo_url)

    # content
    # find the div that contains <p> tags
    paragraphs_div = soup.find_all(property='content:encoded')
    for div in paragraphs_div:
        paragraphs = div.find_all('p')
        for idx, paragraph in enumerate(paragraphs):
            article += str(paragraph)
            article += '\n\r'

            if idx == 0 and img_tag is not None:
                article += img_tag
                article += '\n\r'

    return article


if __name__ == "__main__":
    page = requests.get(
        'http://www.straitstimes.com/business/property', headers=HEADERS)

    if page.status_code != 200:
        sys.exit()

    soup = BeautifulSoup(page.content, 'html.parser')
    result = soup.find_all('a', href=re.compile('/business/property/'))

    for href in result:
        # scrape_article(STRAITSTIME_WEBSITE_URL + href['href'])
        print(scrape_article(STRAITSTIME_WEBSITE_URL + href['href']))
        print('----------------------------------------------------')

    # print(scrape_article(
    # 'http://www.straitstimes.com/business/property/srx-property-first-property-platform-here-to-use-drone-photography-to-market'))
