import requests
from bs4 import BeautifulSoup
from .basescrapper import BaseScrapper

class FetchBeranda(BaseScrapper):
    def __init__(self):
        super().__init__()
        self.LINK = self.BASELINK

    def _getAnime(self, type_list):
        beautifulSoup = BeautifulSoup(self._requestText, features="html.parser")

        # temukan eps
        venutama = beautifulSoup.find('div', class_="venutama")

        if type_list == "ongoing":
            ongoingLi = venutama.find('div',class_='rseries') \
                                .find('div', class_='rapi') \
                                .find('div', class_='venz') \
                                .find_all('li')
        else:
            ongoingLi = venutama.find('div',class_='rseries') \
                                .find('div', class_='rseries') \
                                .find('div', class_='venz') \
                                .find_all('li')

        ongoingList = [x for x in ongoingLi]

        # print(ongoingList)

        result = []

        for ongoing in ongoingList:
            lastUpdate = ongoing.find('div', class_='newnime').get_text().strip()
            totalCurrentEps = ongoing.find('div', class_="epz").get_text().strip()
            updateAt = ongoing.find('div', class_='epztipe').get_text().strip()
            thumbs = ongoing.find('div', class_='thumb')
            animeLink = thumbs.find('a')['href']
            title = thumbs.find('h2', class_='jdlflm').get_text().strip()
            image = thumbs.find('div', class_='thumbz').find('img')['src']

            animeLink = animeLink.replace(self.LINK+"/anime", "").replace("/", "")

            data = {
                "title": title,
                "image": image,
                "animelink": animeLink,
                "lastupdate": lastUpdate,
                "totalcurrenteps": totalCurrentEps,
                "updateat": updateAt
            }
            
            # print(data, end='\n\n')
            result.append(data)
        
        # print(len(result))
        return result

    def getCompleteAnime(self, page)-> list:
        type_list = "complete"
        if not page:
            self._setRequest(self.LINK + '/')
        else:
            self._setRequest(self.LINK + '/complete-anime/page/{}/'.format(str(page)))
            type_list = "ongoing"

        return self._getAnime(type_list)

    def getAllOngoingAnime(self, page):
        
        if not page:
            self._setRequest(self.LINK + '/')
        else:
            self._setRequest(self.LINK + '/ongoing-anime/page/{}/'.format(str(page)))

        return self._getAnime("ongoing")
        
