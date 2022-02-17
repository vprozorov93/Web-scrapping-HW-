import requests
import re
import bs4
from time import time, sleep


def get_my_ip():
    url = 'https://2ip.ru'

    response = requests.get(url)
    response.raise_for_status()

    text = response.text

    soup = bs4.BeautifulSoup(text, features='html.parser')
    ip_address = soup.find(id='d_clip_button').find('span')
    print(ip_address.text)
    ip_address_v2 = re.search(r'\d+\.\d+\.\d+\.\d+', text).group()
    print(ip_address_v2)


def get_habr_text(scrapping_minutes, view_full_text=False):
    end_time = time()+scrapping_minutes*60
    new_paper = []
    while time() < end_time:
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': '',
            'Upgrade-Insecure-Requests': '1'}

        base_url ='https://habr.com'
        url_for_scrapping = 'https://habr.com/ru/all'
        HUBS = ['дизайн', 'фото', 'web', 'python']

        response = requests.get(url_for_scrapping, headers=headers)
        response.raise_for_status()
        text = response.text

        soup = bs4.BeautifulSoup(text, features='html.parser')
        articles = soup.find_all('article')

        for article in articles:
            hubs = article.find_all(class_='tm-article-snippet__hubs-item')
            hubs = [hub.text.strip() for hub in hubs]

            for hub in hubs:
                if hub.lower() in HUBS:
                    href = article.find(class_="tm-article-snippet__title-link").attrs['href']
                    link = base_url + href
                    if link in new_paper:
                        continue
                    new_paper.append(link)
                    date = article.find('time').attrs['title']
                    title = article.find(class_='tm-article-snippet__title tm-article-snippet__title_h2').find('span').text

                    response2 = requests.get(link, headers=headers)
                    response2.raise_for_status()
                    text2 = response2.text
                    soup2 = bs4.BeautifulSoup(text2, features='html.parser')
                    text_page = soup2.find(xmlns="http://www.w3.org/1999/xhtml")

                    valid_text = ''
                    for text in text_page:
                        if text.name == 'p':
                            valid_text += '\n'+text.getText()
                        elif text.name == 'h3':
                            valid_text += '\n'*2+text.getText()

                    print(f'Дата: {date[:date.find(",")]}\nСтатья: {title}\nСсылка: {link})')
                    if view_full_text:
                        print(f'Текст статьи:{valid_text}\n')
                    else:
                        print(f'Текст статьи:{valid_text[:50]}...\n')
        sleep(10)

    print('End of scrapping')


if __name__ == '__main__':
    get_habr_text(0.5)

