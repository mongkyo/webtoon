import requests
from bs4 import BeautifulSoup
import re

from data import Episode, Webtoon


class WebtoonData:
    def __init__(self, title, url_thumbnail, webtoon_id):
        self.title = title
        self.url_webtoon = url_thumbnail
        self.webtoon_id = webtoon_id
    
    def __repr__(self):
        return self.title


class Crawler:
    def show_webtoon_list(self):
        response = requests.get('https://comic.naver.com/webtoon/weekday.nhn')
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        col_list = soup.select_one('div.list_area.daily_all').select('.col')
        li_list = []
        for col in col_list:
            col_li_list = col.select('div.col_inner ul > li')
            li_list.extend(col_li_list)

        webtoon_dict = {}
        for li in li_list:
            href = li.select_one('a.title')['href']
            m = re.search(r'titleId=(\d+)', href)
            webtoon_id = m.group(1)
            title = li.select_one('a.title').get_text(strip=True)
            url_thumbnail = li.select_one('.thumb > a > img')['src']

            if not title in webtoon_dict:
                new_webtoon_list = WebtoonData(title, webtoon_id, url_thumbnail)
                webtoon_dict[title] = new_webtoon_list

        for title, webtoon in webtoon_dict.items():
            print(title)


if __name__ == '__main__':
    crawler = Crawler()
    crawler.show_webtoon_list()
