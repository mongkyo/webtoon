import requests
from bs4 import BeautifulSoup
import re
import os

from data import Episode, Webtoon, WebtoonNotExist



class WebtoonData:
    def __init__(self, title, url_thumbnail, webtoon_id):
        self.title = title
        self.url_webtoon = url_thumbnail
        self.webtoon_id = webtoon_id
    
    def __repr__(self):
        return self.title


class Crawler:
    def __init__(self):
        self._webtoon_dict = {}

    def get_html(self) :
        root = os.path.dirname(os.path.abspath(__name__))
        dir_path = os.path.join(root, 'saved_file')
        file_path = os.path.join(dir_path, 'weekday.html')
        if os.path.exists(file_path):
            html = open(file_path, 'rt').read()
        else:
            os.makedirs(dir_path, exist_ok=True)
            response = requests.get('https://comic.naver.com/webtoon/weekday.nhn')
            html = response.text
            open(file_path, 'wt').write(html)
        return html

    @property
    def webtoon_dict(self):
        if not self._webtoon_dict:
            html = self.get_html()
            soup = BeautifulSoup(html, 'lxml')
            col_list = soup.select_one('div.list_area.daily_all').select('.col')
            li_list = []
            for col in col_list:
                col_li_list = col.select('.col_inner ul > li')
                li_list.extend(col_li_list)

            for li in li_list:
                href = li.select_one('a.title')['href']
                m = re.search(r'titleId=(\d+)', href)
                webtoon_id = m.group(1)
                title = li.select_one('a.title').get_text(strip=True)
                url_thumbnail = li.select_one('.thumb > a > img')['src']

                if not title in self._webtoon_dict:
                    new_webtoon = Webtoon(webtoon_id, title, url_thumbnail)
                    self._webtoon_dict[title] = new_webtoon

        return self._webtoon_dict

    def get_webtoon(self, title):
        try:
            return self.webtoon_dict[title]
        except KeyError:
            raise WebtoonNotExist(title)

    def show_webtoon_list(self):
        for title, webtoon in self.webtoon_dict.items():
            print(title)


if __name__ == '__main__':
    crawler = Crawler()
    w = crawler.get_webtoon('유미의 세포들')
    print(w.episode_dict)
