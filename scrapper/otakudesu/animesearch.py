import requests
from .basescrapper import BaseScrapper
from bs4 import BeautifulSoup

class AnimeSearch(BaseScrapper):
    def __init__(self, query):
        self.query = query.replace(' ', '+')
        self._setRequest('{}?s={}&post_type=anime'.format(self.BASELINK, self.query))

    def otakudesuSearch(self):
        soup = BeautifulSoup(self._requestText, features="html.parser")

        # print(self._requestText)

        venkonten = soup.find('div', id='venkonten')
        page = venkonten.find('div', class_='page')
        searchUl = page.find('ul', class_="chivsrc")

        animes = []

        for anime in searchUl.find_all('li'):
            animeData = {
                "image_url": anime.find('img')['src'],
                "title": anime.find('h2').find('a').text,
                "anime_url": anime.find('h2').find('a')['href']
            }

            for data in anime.find_all('div', class_='set'):
                if data.b.text.lower() == 'genres':
                    animeData[data.b.text] = []
                    for genreA in data.find_all('a'):
                        animeData[data.b.text].append(genreA.text)
                    continue

                animeData[data.b.text] = data.text.strip().replace(' ', '').replace(':', '')
            
            animes.append(animeData)
        
        return animes
                

if __name__ == "__main__":
    s = AnimeSearch("sword art online").otakudesuSearch()
    print(s)
