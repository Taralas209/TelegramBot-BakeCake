import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

access_token = os.getenv('BITLY_ACCESS_TOKEN')  # Загрузка токена из переменных окружения

def shorten_link(original_url, custom_title=None):  # Добавлен custom_title
    bitly_linkshortener_url = 'https://api-ssl.bitly.com/v4/shorten'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    payload = {
        "long_url": original_url,
        "title": custom_title  # Заголовок добавлен в payload
    }
    shortened_link_response = requests.post(bitly_linkshortener_url, headers=headers, json=payload)
    shortened_link_response.raise_for_status()
    shortened_link = shortened_link_response.json()['link']
    return shortened_link

def count_link_clicks(shortened_link):
    parsed_link = urlparse(shortened_link)
    bitly_linkcounter_url = 'https://api-ssl.bitly.com/v4/bitlinks/bit.ly{}/clicks/summary'.format(parsed_link.path)
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    payload = {
        "units": "-1"
    }
    clicks_summary_response = requests.get(bitly_linkcounter_url, headers=headers, params=payload)
    clicks_summary_response.raise_for_status()
    return clicks_summary_response.json()['total_clicks']

def is_bitlink(shortened_link):
    parsed_link = urlparse(shortened_link)
    modified_link = f"{parsed_link.netloc}{parsed_link.path}"
    bitly_linkstatus_url = 'https://api-ssl.bitly.com/v4/bitlinks/{}'.format(modified_link)
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    linkstatus_response = requests.get(bitly_linkstatus_url, headers=headers)
    return linkstatus_response.ok
