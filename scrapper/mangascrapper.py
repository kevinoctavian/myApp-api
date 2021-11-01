import requests
from http.cookiejar import LWPCookieJar
from bs4 import BeautifulSoup
import pprint

flag = ['typeflag Manhwa', 'typeflag Manga', 'typeflag Manhwa']

class MangaScrapper:
    def __init__(self, link = 'https://kiryuu.id'):
        self.link = link
        self._requestText = None
        self.session = self._build_session()

    def _request(self, link:str):
        self._requestText = self.session.get(link).text

    def _build_session(self) -> requests.Session:
        """
        Buat session baru
        """

        session = requests.Session()
        session.headers["User-Agent"] = "Mozilla/5.0 (Linux; Android 7.0; 5060 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36"
        session.cookies = LWPCookieJar()
        return session

    def getHome(self, page = None):
        if page is None:
            self._request(self.link)
        else:
            self._request(self.link+"/page/{}/".format(str(page)))

        soup = BeautifulSoup(self._requestText, "html.parser")
        content = soup.find('div', id="content")
        popular_today = content.find('div', class_='hotslid')
        post_body = content.find('div', class_='postbody')
        # sidebar = content.find('div', id="sidebar")

        result = {}

        # postbody
        for i, post in enumerate(post_body.find_all('div', class_="bixbox")):
            if not post.find('div', class_="series-gen"):
                releases = post.find('div', class_="releases").find("h2")
                # print(releases.text)
                list_upd = post.find('div', class_="listupd").find_all("div", class_="utao")

                result[releases.text] = []
                for upd in list_upd:                        
                    upd_item = {
                        "title": upd.find('div', class_="luf").a.h4.text,
                        "cover": upd.find('div', class_="imgu").img['src'],
                        "link": upd.find('div', class_="imgu").a['href']
                    }

                    if upd.find('div', class_="luf").ul is not None:
                        upd_item['type'] = upd.find('div', class_="luf").ul['class'][0]
                    else:
                        upd_item['type'] = 'Belum Rilis'

                    result[releases.text].append(upd_item)

            elif post.find('div', class_="series-gen"):
                releases = post.find('div', class_="releases").find("h2")
                series_gen = post.find('div', class_="series-gen")

                result[releases.text] = {}
                
                # list_upd = series_gen.find("div", class_="listupd").find_all('div')
                
                # print(pprint.pformat(list_upd))

                for i, rekomendasi in enumerate(series_gen.find_all('li')):
                    try:
                        list_upd = series_gen.find("div", class_="listupd").find_all('div', class_="tab-pane")[i]
                    except IndexError as e:
                        continue

                    result[releases.text][rekomendasi.a.text] = []
                    for bs in list_upd.find_all('div', class_="bs"):
                        bsx = bs.find('div', class_="bsx")

                        if bsx:
                            upd_item = {
                                "title": bsx.a['title'],
                                "cover": bsx.find('div', class_="limit").img['src'],
                                "link": bsx.a['href'],
                                "type": bsx.find('div', class_="limit").find("span", class_="type")['class'][1]
                            }

                            result[releases.text][rekomendasi.a.text].append(upd_item)

                # print("jumlah dari " + releases.text, len(result[releases.text]))

        # hotlist
        for i, post in enumerate(popular_today):
            releases = post.find('div', class_="releases").find("h2")
            # print(releases.text)
            list_upd = post.find('div', class_="listupd").find_all("div", class_="bs")

            result[releases.text] = []
            for upd in list_upd:                        
                bsx = upd.find('div', class_="bsx")

                if bsx:
                    upd_item = {
                        "title": bsx.a['title'],
                        "cover": bsx.find('div', class_="limit").img['src'],
                        "link": bsx.a['href'],
                        "type": bsx.find('div', class_="limit").find("span", class_="type")['class'][1]
                    }

                result[releases.text].append(upd_item)

        # serial populer
        # incomming

        print(pprint.pformat(result))

        return result

    def mangaInfo(self, manga: str):
        manga = manga.replace(f"{self.link}", '')
        self._request(self.link + manga)

        soup = BeautifulSoup(self._requestText, "html.parser")
        post_body = soup.find('div', class_="postbody")

        # information
        information = post_body.find("div", class_="seriestucon")
        genres = information.find('div', class_='seriestucontentr').find('div', class_="seriestugenre").find_all('a')
        information_tables = information.find('div', class_='seriestucontentr').find("table", class_="infotable").find('tbody').find_all('tr')
        sinopsis = information.find('div', class_='seriestucontentr').find('div', class_='entry-content').find_all('p')

        # episodes
        chapters = post_body.find("div", class_="epcheck").find('ul', class_='clstyle').find_all('li')

        # "\n".join(.find('div', class_='entry-content').find_all('p'))
        result = {
            "title": information.find("div", class_="seriestuheader").h1.text,
            "title_alternatif": information.find("div", class_="seriestuheader").div.text.strip(),
            "sinopsis": '\n'.join([x.text for x in sinopsis]),
            "information": {},
            "chapters": [],
            "genres": []
        }

        # chapters loop
        for chapter in chapters:
            chapter_item = {
                "title": chapter.find("div", class_="eph-num").a.find("span", class_="chapternum").text,
                "link": chapter.find("div", class_="eph-num").a['href'],
                "updateat": chapter.find("div", class_="eph-num").a.find("span", class_="chapterdate").text
            }

            result['chapters'].append(chapter_item)

        # genre loop
        for genre in genres:
            genre_item = {
                "title": genre.text,
                "link": genre['href']
            }
            result['genres'].append(genre_item)

        # information loop
        for informa in information_tables:
            td = informa.find_all('td')
            result['information'][td[0].text.lower().replace(' ', '')] = td[1].text

        return result

    def getManga(self, manga: str):
        manga = manga.replace(f"{self.link}", '')
        self._request(self.link + manga)
        
        soup = BeautifulSoup(self._requestText, "html.parser")
        post_area = soup.find('div', class_="postarea")

        result = []

        for manga_img in post_area.find("div", id="readerarea").find_all('img'):
            result.append(manga_img['src'])

        
        return result

    def searchManga(self, query: str, page: str = None):
        query = query.replace(f"{self.link}", '')
        if page is not None:
            self._request("%s/page/%s/?s=%s" % (self.link, page, query))
        else:
            self._request("%s/?s=%s" % (self.link, query))

        soup = BeautifulSoup(self._requestText, "html.parser")
        post_body = soup.find("div", class_="postbody")
        
        result = {
            "manga_result": []
        }

        # scrap for manga
        for manga_search in post_body.find("div", class_="listupd").find_all("div", class_="bs"):
            bsx = manga_search.find("div", class_="bsx")

            manga_item = {
                "title": bsx.a['title'],
                "cover": bsx.find('div', class_="limit").img['src'],
                "link": bsx.a['href'],
                "type": bsx.find('div', class_="limit").find("span", class_="type")['class'][1],
                "chapter": bsx.find('div', class_="epxs").text
            }

            result['manga_result'].append(manga_item)

        # scrap for pagenation
        pagination = post_body.find("div", class_="pagination")
        max_page = pagination.find_all("a", class_="page-numbers")

        if max_page:
            if len(max_page) >= 4:
                max_page = max_page[2]
                result['max_page'] = int(max_page.text)
            elif len(max_page) == 3:
                max_page = max_page[1]
                result['max_page'] = int(max_page.text)
            elif len(max_page) == 2:
                max_page = max_page[0]
                result['max_page'] = int(max_page.text)
        
        return result

    def getMangaList(self, option):
        pass

    def _isLink(self, link: str):
        print(link)
        return link.startswith('http') or link.startswith('https')

if __name__ == "__main__":
    manga = MangaScrapper().getHome()