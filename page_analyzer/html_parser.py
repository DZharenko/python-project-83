import requests
from bs4 import BeautifulSoup


def html_parser(url):

    result = {}

    try:
        response = requests.get(url)
        response.raise_for_status()

        response.encoding = 'utf-8'
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        result["h1"] = soup.h1.get_text(strip=True) if soup.h1 else None
        result["title"] = (
            soup.title.get_text(strip=True) if soup.title else None
        )

        meta_tag = soup.find('meta', attrs={'name': 'description'})
        result["description"] = (
            meta_tag.get('content', '').strip() if meta_tag else None
        )

        return result
    
    except requests.exceptions.RequestException as e:
        return f'Ошибка запроса: {e}'
