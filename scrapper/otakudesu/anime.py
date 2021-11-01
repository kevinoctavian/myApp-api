import requests
from bs4 import BeautifulSoup
from .basescrapper import BaseScrapper

class AnimeFetch(BaseScrapper):
    def __init__(self, link):
        super().__init__()
        
        self.link = link
        self._setRequest(self.link)

    def getEpisodesOtakudesu(self):
        # class_='episodelist'

        beautifulSoup = BeautifulSoup(self._requestText, features="html.parser")

        # temukan eps
        episodeList = beautifulSoup.find('div', id='venkonten').find_all('div', class_='episodelist')[1]
        ongoingLi = episodeList.find('ul').find_all('li')

        # sinopsis
        sinopsis = beautifulSoup.find("div", class_="sinopc").find_all("p")

        # info
        infos = beautifulSoup.find("div", class_="infozingle").find_all("p")

        ongoingList = [x for x in ongoingLi]
        sinopsis = [p.text for p in sinopsis]
        infos = [info.span.text for info in infos]

        result = {
            "anime": [],
            "sinopsis": "\n".join(sinopsis),
            "info": "\n".join(infos)
        }

        for ongoing in ongoingList:
            animeLink = ongoing.find('a')
            title = animeLink.get_text()
            # updateAt = ongoing.find('span', class_='zeebr').get_text()

            data = {
                "title": title,
                "animelink": animeLink['href']
            }
            
            result['anime'].append(data)
        
        # print(result['info'])

        return result

    def getEpisodesNekonime(self):
        # class_='episodelist'
        beautifulSoup = BeautifulSoup(self._requestText, features="html.parser")

        # temukan eps
        episodeList = beautifulSoup.find('div', id='venkonten').find_all('div', class_='episodelist')[1]
        ongoingLi = episodeList.find('ul').find_all('li')

        ongoingList = [x for x in ongoingLi]

        result = []

        for ongoing in ongoingList:
            animeLink = ongoing.find('a')
            title = animeLink.get_text()
            # updateAt = ongoing.find('span', class_='zeebr').get_text()

            data = {
                "title": title,
                "animelink": animeLink['href']
            }
            
            result.append(data)
        
        return result


    
if __name__ == '__main__':
    AnimeFetch('https://animasu.net/anime/super-cub/')