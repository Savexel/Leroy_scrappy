import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

Url = input('скопируйте сюда ссылку на категорию товаров// пример: https://leroymerlin.ru/catalogue/laminat/ ')
Headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
           'accept': '*/*'}
FILE = 'Leroy.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=Headers, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='bex6mjh_plp b1f5t594_plp iypgduq_plp nf842wf_plp')
    prices = soup.find_all('div', class_='oo1t094_plp largeCard')
    items_list = []
    for item in items:
        for pr_item in prices:
            items_list.append({
                'Название': item.find('span', class_='cef202m_plp').
                    find_next('span', class_='t9jup0e_plp p1h8lbu4_plp').get_text(),
                'Цена (rub)': pr_item.find('div', {'class': 'p1nn3tkz_plp'}).find_next('div', {
                    'data-qa': 'product-primary-price'}).
                    find_next('p', class_='t3y6ha_plp xc1n09g_plp p1q9hgmc_plp').get_text().replace('\xa0', '')
            })
    df = pd.DataFrame(items_list)
    df.to_csv(FILE, sep=';', encoding="utf-8-sig")
    return print('Файл сформирован ', df.head())


def parse():
    html = get_html(Url)
    if html.status_code == 200:
        items_list = get_content(html.text)
    else:
        print('ERR!!!', '\n', 'No connection!')
    print('\n', html)


parse()
# to create an exe: in TERMINAL: pyinstaller --onefile Leroy_scrappy.py
