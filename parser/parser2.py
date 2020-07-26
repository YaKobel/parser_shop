import requests
from bs4 import BeautifulSoup
import csv

HOST = 'https://minfin.com.ua/'
URL = 'https://minfin.com.ua/cards/'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'
}

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='product-item')
    cards = []
    print(items)


html = get_html(URL)
get_content(html.text)