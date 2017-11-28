from pprint import pprint
from urllib.parse import urlencode, urljoin

import requests

AUTH_URL = 'https://oauth.yandex.ru/authorize'
APP_ID = 'eecce992e7624ee6a9a96a69562870ce'

auth_data = {
    'response_type': 'token',
    'client_id': APP_ID
}

print('?'.join((AUTH_URL, urlencode(auth_data))))

TOKEN = 'AQAAAAAapLk7AAStTRwTO7KCVkpvq6baHa771X0'


class YMBase:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Authorization': 'OAuth {}'.format(self.token),
            'Content-Type': 'application/x-yametrika+json'
        }


class YMUser(YMBase):
    MANANGMENT_URL = 'https://api-metrika.yandex.ru/management/v1/'

    def get_counters(self):
        headers = self.get_headers()

        response = requests.get(

            urljoin(self.MANANGMENT_URL, 'counters'),
            headers=headers

        )

        return response.json()['counters']

    def get_counters_info(self, counter_id):
        headers = self.get_headers()

        response = requests.get(

            urljoin(self.MANANGMENT_URL, 'counter/{}'.format(counter_id)),
            headers=headers
        )
        return response.json()

    def get_counter_filters(self, counter_id):
        headers = self.get_headers()

        response = requests.get(
            urljoin(self.MANANGMENT_URL, 'counter/{}/filters'.format(counter_id)),
            headers=headers
        )
        return response.json()

    def get_counter_grands(self, counter_id):
        headers = self.get_headers()

        response = requests.get(
            urljoin(self.MANANGMENT_URL, 'counter/{}/grants'.format(counter_id)),
            headers=headers
        )
        return response.json()


class Counter(YMBase):
    STAT_URL = 'https://api-metrika.yandex.ru/stat/v1/data'

    def __init__(self, id, token):
        self.id = id
        super().__init__(token)

    def get_base_mentrics(self, metric):
        headers = self.get_headers()
        params = {
            'id': self.id,
            'metrics': metric
        }
        response = requests.get(self.STAT_URL, params, headers=headers)
        return response.json()


ilyaaa = YMUser(TOKEN)
counters = ilyaaa.get_counters()
for c in counters:
    pprint(ilyaaa.get_counters_info(c['id']))
    print('----------------------------------------------------------')
    pprint(ilyaaa.get_counter_filters(c['id']))
    print('----------------------------------------------------------')
    pprint(ilyaaa.get_counter_grands(c['id']))
    print('----------------------------------------------------------')
    counter = Counter(c['id'], TOKEN)
    pprint(counter.get_base_mentrics('ym:s:visits'))  # Суммарное количество визитов
    print('----------------------------------------------------------')
    pprint(counter.get_base_mentrics('ym:s:pageviews'))  # Число просмотров страниц на сайте за отчетный период
    print('----------------------------------------------------------')
    pprint(counter.get_base_mentrics('ym:s:users'))  # Количество уникальных посетителей
    print('----------------------------------------------------------')
    pprint(counter.get_base_mentrics('ym:s:percentNewVisitors'))



