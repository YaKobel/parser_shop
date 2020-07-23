import logging
import collections

import bs4
import requests


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('parser')


ParseResult = collections.namedtuple(
    'ParseResult',
    (
        'brand_name',
        'goods_name',
        'url',
    ),
)


class Client:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
            'accept': '*/*'
        }
        self.result = []

    def load_page(self):
        url = 'https://www.wildberries.ru/catalog/muzhchinam/odezhda/vodolazki'
        res = self.session.get(url=url)
        res.raise_for_status()
        return res.text

    def parse_page(self, text: str):
        soup = bs4.BeautifulSoup(text, 'lxml')
        container = soup.select('div.dtList-inner')
        for block in container:
            self.parse_block(block=block)

    def parse_block(self, block):
        # logger.info(block)
        # logger.info('=', * 100)

        url_block = block.select_one('a.ref_goods_n_p.j-open-full-product-card')
        if not url_block:
            logger.error('no url_block')
            return

        url = url_block.get('href')
        if not url:
            logger.error('no href')
            return

        name_block = block.select_one('div.dtlist-inner-brand-name')
        if not name_block:
            logger.error(f'no name_block on {url}')
            return

        brand_name = name_block.select_one('strong.brand-name')
        if not brand_name:
            logger.error(f'no name_block on {url}')
            return

        # Wrangler /
        brand_name = brand_name.text
        brand_name = brand_name.replace('/', '').strip()

        goods_name = name_block.select_one('span.goods-name.c-text-sm')
        if not goods_name:
            logger.error(f'no goods_name on {url}')
            return

        goods_name = goods_name.text.strip()

        logger.info('%s, %s, %s', url, brand_name, goods_name)


    def run(self):
        text = self.load_page()
        self.parse_page(text=text)

if __name__ == '__main__':
    parser = Client()
    parser.run()








# URL = 'https://auto.ria.com/newauto/marka-jeep'
# HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0', 'accept': '*/*'}
# HOST = 'https://auto.ria.com'
# FILE = 'cars.csv'

# 'User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'