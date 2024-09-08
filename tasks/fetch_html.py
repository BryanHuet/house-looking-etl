from prefect import task
import requests
from bs4 import BeautifulSoup


@task
def fetch_html_page(url: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko)'
                      'Chrome/85.0.4183.121 Safari/537.36',
        'Referer': url,  # Set the referer to the same site
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',  # Browser usually sends this
        'Connection': 'keep-alive',
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception if the request failed
    return response.content


@task
def parse_html(html: str, balise: str, value):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all(balise, value)
