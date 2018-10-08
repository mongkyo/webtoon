import re
from collections import OrderedDict

import requests
from bs4 import BeautifulSoup

from . import Episode

__all__ = (
    'Webtoon',
    'WebtoonNotExist',
)


class Webtoon:
    TEST_WEBTOON_ID = 714843

    def __init__(self, webtoon_id, title, url_thumbnail):
        self.webtoon_id = webtoon_id
        self.title = title
        self.url_thumbnail = url_thumbnail
        self._episode_dict = OrderedDict()

    def __repr__(self):
        return self.title

    @property
    def url(self):
        return f'https://comic.naver.com/webtoon/list.nhn?titleId={self.webtoon_id}'


    @property
    def episode_dict(self):
        if not self._episode_dict:
            #
            #
            response = requests.get(self.url)
            soup = BeautifulSoup(response.text, 'lxml')

            #
            table = soup.select_one('table.viewList')
            tr_list = table.select('tr')[1:]
            for tr in tr_list:
                #
                try:
                    td_list = tr.select('td')
                    href = td_list[0].select_one('a')['href']
                    no = re.search(r'no=(\d+)', href).group(1)
                    url_thumbnail = td_list[0].select_one('img')['src']
                    title = td_list[1].select_one('a').get_text(strip=True)
                    rating = td_list[2].select_one('strong').get_text()
                    created_date = td_list[3].get_text(strip=True)

                    episode = Episode(
                        episode_id=no,
                        title=title,
                        url_thumbnail=url_thumbnail,
                        rating=rating,
                        created_date=created_date,
                    )
                    #
                    self._episode_dict[no] = episode
                except:
                    pass
        return self._episode_dict

    def get_episode(self, index):
        pass


class Webtoon_all_page:
    TEST_WEBTOON_ID = 714843

    def __init__(self, webtoon_id, title, url_thumbnail):
        self.webtoon_id = webtoon_id
        self.title = title
        self.url_thumbnail = url_thumbnail
        self._episode_dict = OrderedDict()
        self.new_page = 1
        self.old_page = 1

    def __repr__(self):
        return self.title

    @property
    def url_page(self):
        return f'https://comic.naver.com/webtoon/list.nhn?titleId=711899&weekday=mon&page={self.new_page}'

    response = requests.get(self.url_page)
    container = soup.select_one('div.webtoon')
    page_wrap = container.select_one('div.page_wrap')
    strong_num = page_wrap.select_one('strong.page')
    now_page = strong_num.select_one('em.num_page').get_text(strip=True)
    new_page = int(now_page)
    old_page = new_page
    new_page += 1





    @property
    def episode_dict(self):
        if not self._episode_dict:
            #
            #
            response = requests.get(self.url_page)
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            #
            container = soup.select_one('div.webtoon')
            page_wrap = container.select_one('div.page_wrap')
            strong_num = page_wrap.select_one('strong.page')
            now_page = strong_num.select_one('em.num_page').get_text(strip=True)
            new_page = int(now_page)
            old_page = new_page
            new_page += 1
            table = soup.select_one('table.viewList')
            tr_list = table.select('tr')[1:]
            for tr in tr_list:
                #
                try:
                    td_list = tr.select('td')
                    href = td_list[0].select_one('a')['href']
                    no = re.search(r'no=(\d+)', href).group(1)
                    url_thumbnail = td_list[0].select_one('img')['src']
                    title = td_list[1].select_one('a').get_text(strip=True)
                    rating = td_list[2].select_one('strong').get_text()
                    created_date = td_list[3].get_text(strip=True)

                    episode = Episode(
                        episode_id=no,
                        title=title,
                        url_thumbnail=url_thumbnail,
                        rating=rating,
                        created_date=created_date,
                    )
                    #
                    self._episode_dict[no] = episode
                except:
                    pass
            while new_page != old_page:
                test_url = f'https://comic.naver.com/webtoon/list.nhn?titleId=711899&weekday=mon&page={new_page}'
                response = requests.get(test_url)
                html = response.text
                soup = BeautifulSoup(html, 'lxml')
                container = soup.select_one('div.webtoon')
                page_wrap = container.select_one('div.page_wrap')
                strong_num = page_wrap.select_one('strong.page')
                now_page = strong_num.select_one('em.num_page').get_text(strip=True)
                new_page = int(now_page)
                if new_page > old_page:
                    old_page = new_page
                    new_page += 1
                    table = soup.select_one('table.viewList')
                    tr_list = table.select('tr')[1:]
                    for tr in tr_list:
                        #
                        try:
                            td_list = tr.select('td')
                            href = td_list[0].select_one('a')['href']
                            no = re.search(r'no=(\d+)', href).group(1)
                            url_thumbnail = td_list[0].select_one('img')['src']
                            title = td_list[1].select_one('a').get_text(strip=True)
                            rating = td_list[2].select_one('strong').get_text()
                            created_date = td_list[3].get_text(strip=True)

                            episode = Episode(
                                episode_id=no,
                                title=title,
                                url_thumbnail=url_thumbnail,
                                rating=rating,
                                created_date=created_date,
                            )
                            #
                            self._episode_dict[no] = episode
                        except:
                            pass
            #     else:
            #         pass
            #
            # table = soup.select_one('table.viewList')
            # tr_list = table.select('tr')[1:]
            # for tr in tr_list:
            #     #
            #     try:
            #         td_list = tr.select('td')
            #         href = td_list[0].select_one('a')['href']
            #         no = re.search(r'no=(\d+)', href).group(1)
            #         url_thumbnail = td_list[0].select_one('img')['src']
            #         title = td_list[1].select_one('a').get_text(strip=True)
            #         rating = td_list[2].select_one('strong').get_text()
            #         created_date = td_list[3].get_text(strip=True)
            #
            #         episode = Episode(
            #             episode_id=no,
            #             title=title,
            #             url_thumbnail=url_thumbnail,
            #             rating=rating,
            #             created_date=created_date,
            #         )
            #         #
            #         self._episode_dict[no] = episode
            #     except:
            #         pass
        return self._episode_dict

    def get_episode(self, index):
        pass


class WebtoonNotExist(Exception):
    def __init__(self, title):
        self.title = title

    def __str__(self):
        return f'Webtoon ( title : {self.title} )을 찾을 수 없습니다.'
