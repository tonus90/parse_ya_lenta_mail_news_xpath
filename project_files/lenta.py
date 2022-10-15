from time import strftime
import requests
from lxml import html
from pprint import pprint
from urllib.parse import urljoin
import datetime
from pymongo import MongoClient
from time import sleep


header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'}

url = 'https://lenta.ru/'
response = requests.get(url, headers=header)

dom = html.fromstring(response.text)
items = dom.xpath('//a[@class="card-mini _topnews"] | //div[@class="topnews__first-topic"]')

client = MongoClient('localhost', 27017)
db = client['news']
news_lenta = db['news_lenta']

def save_news(collection):
    sleep(0.2)
    news_lenta.insert_one(collection)


def get_datetime(list_with_date):
    months = {
        'янв': 1,
        'фев': 2,
        'мар': 3,
        'апр': 4,
        'май': 5,
        'июн': 6,
        'июл': 7,
        'авг': 8,
        'сен': 9,
        'окт': 10,
        'ноя': 11,
        'дек': 12,
    }

    for element in list_with_date:
        # if element.find(':') != -1:
        #     time = element.split(':')
        #     hour = int(time[0])
        #     minute = int(time[1])
        # else:
        #     date = element.split(' ')
        #     day = int(date[1])
        #     month = int(months[date[2][:3:]])
        #     year = int(date[3])

        today = f"{datetime.date.today().strftime('%Y/%m/%d')} {element}"
        date_res = datetime.datetime.strptime(today, '%Y/%m/%d %H:%M')
    return date_res

def name_corrector(name):
    return name.replace(u'\xa0', ' ')


for item in items:
    data = {}
    if item.attrib['class'] == 'topnews__first-topic':
        name = item.xpath('.//h3/text()')[0]
        url_news = urljoin(url, item.xpath('./a/@href')[0])
        date_time = item.xpath(".//time[@class='card-big__date']/text()")
        source = 'https://lenta.ru/'
    else:
        name = item.xpath('.//span[@class = "card-mini__title"]/text()')[0]
        print(item.attrib['href'])
        url_news = urljoin(url, item.attrib['href'])
        date_time = item.xpath(".//time[@class='card-mini__date']/text()")
        source = 'https://lenta.ru/'

    data['name'] = name_corrector(name)
    data['url'] = url_news
    data['date'] = get_datetime(date_time)
    data['source'] = source
    sleep(0.2)
    save_news(data)







