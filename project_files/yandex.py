import requests
from lxml import html
from pprint import pprint
from urllib.parse import urljoin
import datetime
from pymongo import MongoClient

header = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

url = 'https://yandex.ru/news/'
response = requests.get(url, headers=header)

dom = html.fromstring(response.text)
block_top_news = dom.xpath('//div')[0]
items = block_top_news.xpath('.//div[@class="mg-grid__col mg-grid__col_xs_8"] | .//div[@class="mg-grid__col mg-grid__col_xs_4"]')
print(1)

client = MongoClient('localhost', 27017)
db = client['news']
news_yandex = db['news_yandex']

def save_news(collection):
    news_yandex.insert_one(collection)


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


for item in items:
    data = {}
    name = item.xpath('.//a/h2/text()')[0]
    url_news = item.xpath('.//a/@href')[0]
    date_time = item.xpath('.//span[@class = "mg-card-source__time"]/text()')[0]
    source = item.xpath('.//span[@class = "mg-favorites-dot__indicator mg-favorites-dot__indicator_size_s"]/a/text()')[0]

    data['name'] = name_corrector(name)
    data['url'] = url_news
    data['date'] = get_datetime(date_time)
    data['source'] = source
    print(1)
    save_news(data)







