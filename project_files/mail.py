import requests
from lxml import html
from pprint import pprint
from urllib.parse import urljoin
import datetime
from pymongo import MongoClient

header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'}

url = 'https://news.mail.ru/'
response = requests.get(url, headers=header)

dom = html.fromstring(response.text)
block_news = dom.xpath('//a[@class="photo photo_full photo_scale js-topnews__item"]//@href | //a[@class="photo photo_small photo_scale photo_full js-topnews__item"]//@href')


client = MongoClient('localhost', 27017)
db = client['news']
news_mail = db['news_mail']

def save_news(collection):
    news_mail.insert_one(collection)

def get_datetime(time):
    year = datetime.date.today().year
    month = datetime.date.today().month
    day = datetime.date.today().day
    time = time.split(':')
    hour = int(time[0])
    minute = int(time[1])
    date_res = datetime.datetime(year, month, day, hour=hour, minute=minute)
    return date_res

def name_corrector(name):
    return name.replace(u'\xa0', ' ')

for url_news in block_news:
    response_news = requests.get(url_news, headers=header)
    dom_news = html.fromstring(response_news.text)
    data = {}
    name = dom_news.xpath('.//h1/text()')[0]
    date_time = dom_news.xpath('.//span[@class="note"]//@datetime')[0]
    # date = datetime.datetime.strptime(date_time, '%Y%m%d').date()
    
    source = dom_news.xpath('//span[@class="link__text"]/text()')[0]
    
    data['name'] = name_corrector(name)
    data['url'] = url_news
    data['date'] = date_time
    data['source'] = source
    save_news(data)



