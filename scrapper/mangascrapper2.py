import requests
from http.cookiejar import LWPCookieJar
from bs4 import BeautifulSoup
import pprint
import time

class MangaScrapper:
    def __init__(self, link = 'https://komiku.id/'):
        self.link = link
        self._requestText = None
        # self.driver = self._build_driver()
        self.session = self._build_session()

    def _request(self, link:str, **option) -> requests.Response:
        sesion = self.session.get(link, **option)
        self._requestText = sesion.text
        return sesion

    def _build_session(self) -> requests.Session:
        """
        Buat session baru
        """

        session = requests.Session()
        session.headers[
            "User-Agent"] = "Mozilla/5.0 (Linux; Android 7.0; 5060 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36"
        session.cookies = LWPCookieJar()
        return session

    def getHome(self):
        req = self._request(self.link)

        soup = BeautifulSoup(self._requestText, "html.parser")
        kontent = soup.find("div", class_="konten")

        komik_hot = kontent.find("section", id="Komik_Hot")
        komik_terbaru = kontent.find_all("section", id="Terbaru")[1:]

        result = {}

        # print(self._requestText, "\n\n")
        # print(komik_hot, "\n\n")
        # print(komik_terbaru[0].prettify())

        #project
        result['project'] = []
        for komik in komik_terbaru[0].find_all("div", class_="ls4"):
            item1 = komik.find("div", class_="ls4v")
            item2 = komik.find("div", class_="ls4j")

            komik_item = {
                "title": item2.h4.a.text,
                "url": self._fixUrl(item1.a['href']),
                "cover": item1.a.img['data-src'],
                "info": (item1.find(class_='vw').text + "view • " + item2.find("span", class_='ls4s').text).strip(),
                "is_color": True if item1.find(class_='warna') else False,
                "chapter": {
                    "title": item2.find("a", class_="ls24").text,
                    "link": self._fixUrl(item2.find("a", class_="ls24")['href'])
                }
            } 

            result['project'].append(komik_item)

        #Update terbaru
        result['update_terbaru'] = []
        for komik in komik_terbaru[1].find_all("div", class_="ls4"):
            item1 = komik.find("div", class_="ls4v")
            item2 = komik.find("div", class_="ls4j")

            komik_item = {
                "title": item2.h4.a.text,
                "url": self._fixUrl(item1.a['href']),
                "cover": item1.a.img['data-src'],
                "info": (item1.find(class_='vw').text + "view • " + item2.find("span", class_='ls4s').text).strip(),
                "is_color": True if item1.find(class_='warna') else False,
                "chapter": {
                    "title": item2.find("a", class_="ls24").text,
                    "link": self._fixUrl(item2.find("a", class_="ls24")['href'])
                }
            } 

            result['update_terbaru'].append(komik_item)
        
        # Manga populer
        result['manga_populer'] = []
        for komik in komik_hot.find_all("div", class_="perapih")[0].find_all("div", class_="ls2"):
            # print(komik.prettify())
            item1 = komik.find("div", class_="ls2v")
            item2 = komik.find("div", class_="ls2j")

            komik_item = {
                "title": item2.h4.a.text,
                "url": self._fixUrl(item1.a['href']),
                "cover": item1.a.img['data-src'],
                "info": (item1.find(class_='vw').text + "view • " + item2.find("span", class_='ls2t').text).strip(),
                "is_color": True if item1.find(class_='warna') else False,
                "chapter": {
                    "title": item2.find("a", class_="ls2l").text,
                    "link": self._fixUrl(item2.find("a", class_="ls2l")['href'])
                }
            } 

            result['manga_populer'].append(komik_item)

        # hot hari ini
        result['hot_hari_ini'] = []
        for komik in komik_hot.find_all("div", class_="perapih")[1].find_all("div", class_="ls2"):
            # print(komik.prettify())
            item1 = komik.find("div", class_="ls2v")
            item2 = komik.find("div", class_="ls2j")

            komik_item = {
                "title": item2.h4.a.text,
                "url": self._fixUrl(item1.a['href']),
                "cover": item1.a.img['data-src'],
                "info": (item1.find(class_='vw').text + "view • " + item2.find("span", class_='ls2t').text).strip(),
                "is_color": True if item1.find(class_='warna') else False,
                "chapter": {
                    "title": item2.find("a", class_="ls2l").text,
                    "link": self._fixUrl(item2.find("a", class_="ls2l")['href'])
                }
            } 

            result['hot_hari_ini'].append(komik_item)

        # print(pprint.pformat(result))
        # self.driver.close()
        return result

    def _fixUrl(self, url: str):
        if not url.startswith(self.link):
            if url.startswith('/'):
                url = url[1:]
            return self.link + url
        
        return url

    def mangaInfo(self, manga: str):
        manga = manga.replace(f"{self.link}", '')
        self._request(self.link + manga)

        soup = BeautifulSoup(self._requestText, "html.parser")
        main = soup.find('main', class_="perapih")

        # information
        title = main.find("header", id="Judul").h1.text.strip()
        sinopsis = main.find("section", id="Sinopsis").find_all("p")[-1].text.strip()

        informasi = main.find("section", id="Informasi")

        # cover
        cover = informasi.find(class_="ims").img['src']

        # info table
        info_table = informasi.find("table", class_="inftable").find_all("tr")

        # genre
        genres = informasi.find("ul", class_="genre").find_all("li")

        # mirip
        manga_mirip = main.find("section", id="Spoiler").find_all(class_="grd")

        # chapter
        chapters = main.find("section", id="Chapter").find('table', id='Daftar_Chapter').find_all('tr')[1:]

        # "\n".join(.find('div', class_='entry-content').find_all('p'))
        result = {
            "title": title,
            "cover": cover,
            "sinopsis": sinopsis,
            "information": {},
            "chapters": [],
            "genres": [],
            "manga_mirip": []
        }

        # chapters loop
        for chapter in chapters:
            chapter_item = {
                "title": chapter.find("td", class_="judulseries").a.text.strip(),
                "link": self._fixUrl(chapter.find("td", class_="judulseries").a['href']),
                "updateat": chapter.find("td", class_="tanggalseries").text.strip()
            }

            result['chapters'].append(chapter_item)

        # genre loop
        for genre in genres:
            genre_item = {
                "title": genre.a.text,
                "link": self._fixUrl(genre.a['href'])
            }

            result['genres'].append(genre_item)

        # information loop
        for informa in info_table:
            td = informa.find_all('td')
            result['information'][td[0].text] = td[1].text

        # mirip loop
        for mirip in manga_mirip:
            mirip_item = {
                "title": mirip.a.find(class_="h4").text.strip(),
                "cover": mirip.a.find("img")['data-src'],
                "link": self._fixUrl(mirip.a['href']),
                "info": (mirip.find(class_='vw').text + " view • " + mirip.find(class_='tpe1_inf').b.text + mirip.find(class_='tpe1_inf').text).strip().replace('\t', ''),
                "sinopsis": mirip.find("p").text.strip()
            }

            result['manga_mirip'].append(mirip_item)

        # print(pprint.pformat(result))

        return result

    def getManga(self, manga: str):
        manga = manga.replace(f"{self.link}", '')
        self._request(self.link + manga)
        
        soup = BeautifulSoup(self._requestText, "html.parser")
        baca_komik = soup.find('section', id="Baca_Komik")

        # print(soup.prettify())

        result = {
            "manga": [],
            "title": soup.find("header", id="Judul").h1.text.replace('\t', '').replace('\n', ''),
            "cara_baca": soup.find("table", class_="tbl").find_all('td')[1].text
        }

        for manga_img in baca_komik.find_all('img'):
            result['manga'].append(manga_img['src'])

        return result

    def searchManga(self, query: str, page: str = None):
        query = query.replace(f"{self.link}", '')
        
        if page is not None:
            req = self._request(self.link + f"cari/page/{page}/", params = {"post_type": "manga", "s": query})       
        else:
            req = self._request(self.link + "cari/", params = {"post_type": "manga", "s": query})

        soup = BeautifulSoup(self._requestText, "html.parser")
        daftar = soup.find("div", class_="daftar")
        genres = soup.find("div", id="genr").find("ul", class_="genre")

        if not daftar:
            return {"error": {"msg", "data kosong"}}

        result = {
            "manga_result": [],
            "semua_genre": [],
            "page_selanjutnya": False, 
            "page_sebelumnya": False
        }

        pages = soup.find("div", class_="pag-nav")

        if pages:
            result['page_selanjutnya'] = True if pages.find("a", class_="next") else False
            result['page_sebelumnya'] = True if pages.find("a", class_="prev") else False

        # scrap for manga
        for manga_search in daftar.find_all("div", class_="bge"):
            item1 = manga_search.find("div", class_="bgei")
            item2 = manga_search.find("div", class_="kan")
            chapters = item2.find_all("div", class_="new1")

            komik_item = {
                "title": item2.a.h3.text.replace('\t', '').replace('\n','').strip(),
                "url": self._fixUrl(item1.a['href']),
                "cover": item1.a.img['data-src'],
                "info": item2.p.text.replace('\t', '').replace('\n','').strip(),
                "type": (item1.find("div", class_="tpe1_inf").text).replace('\n',' ').strip(),
                "chapter": {
                    "Awal": {
                        "title": chapters[0].a.find_all("span")[1].text,
                        "link": self._fixUrl(chapters[0].a['href'])
                    },
                    "Terbaru": {
                        "title": chapters[1].a.find_all("span")[1].text,
                        "link": self._fixUrl(chapters[1].a['href'])
                    }
                }
            }   

            result['manga_result'].append(komik_item)
        
        # scrap for genre
        for genre in genres.find_all("li"):
            # print(genre)
            result['semua_genre'].append({
                "title": genre.a.text,
                "url": self._fixUrl(genre.a['href'])
            })

        return result

    def mangaPustaka(self, page: str = None, option:dict=None):
        if page == '1' or page == 1:
            page = None
            

        if option:

            options = {}
            for key, value in option.items():
                if value:
                    options[key] = value

            if page is not None:
                req = self._request(f"{self.link}pustaka/page/{page}/", params=options)       
            else:
                req = self._request(self.link + "pustaka/", params=options)
        else:
            if page is not None:
                req = self._request(f"{self.link}pustaka/page/{page}/")       
            else:
                req = self._request(self.link + "pustaka/")

        soup = BeautifulSoup(self._requestText, "html.parser")
        daftar = soup.find("div", class_="daftar")
        genres = soup.find("div", id="genr").find("ul", class_="genre")

        if not daftar:
            return {"error": {"msg", "data kosong"}}

        result = {
            "manga_result": [],
            "semua_genre": [],
            "page_selanjutnya": False, 
            "page_sebelumnya": False
        }

        pages = soup.find("div", class_="pag-nav")

        if pages:
            result['page_selanjutnya'] = True if pages.find("a", class_="next") else False
            result['page_sebelumnya'] = True if pages.find("a", class_="prev") else False

        # scrap for manga
        for manga_search in daftar.find_all("div", class_="bge"):
            item1 = manga_search.find("div", class_="bgei")
            item2 = manga_search.find("div", class_="kan")
            chapters = item2.find_all("div", class_="new1")

            komik_item = {
                "title": item2.a.h3.text.replace('\t', '').replace('\n','').strip(),
                "url": self._fixUrl(item1.a['href']),
                "cover": self._fixImgSource(item1.a.img['data-src']),
                "info": item2.p.text.replace('\t', '').replace('\n','').strip(),
                "type": (item1.find("div", class_="tpe1_inf").text).replace('\n',' ').strip(),
                "chapter": {
                    "Awal": {
                        "title": chapters[0].a.find_all("span")[1].text,
                        "link": self._fixUrl(chapters[0].a['href'])
                    },
                    "Terbaru": {
                        "title": chapters[1].a.find_all("span")[1].text,
                        "link": self._fixUrl(chapters[1].a['href'])
                    }
                }
            }   

            result['manga_result'].append(komik_item)
        
        # scrap for genre
        for genre in genres.find_all("li"):
            # print(genre)
            result['semua_genre'].append({
                "title": genre.a.text,
                "url": self._fixUrl(genre.a['href'])
            })

        return result

    def searchByGenre(self, genre:str, page:str = None, param = None):
        genre = genre.lower()
        if param:
            options = {}
            for key, value in option.items():
                if value:
                    options[key] = value

            if page is not None:
                req = self._request(self.link + f"genre/{genre}/page/{page}/", params=options)       
            else:
                req = self._request(self.link + f"genre/{genre}/", params=options)
        else:
            if page is not None:
                req = self._request(self.link + f"genre/{genre}/page/{page}/")       
            else:
                req = self._request(self.link + f"genre/{genre}/")

        soup = BeautifulSoup(self._requestText, "html.parser")
        daftar = soup.find("div", class_="daftar")
        genres = soup.find("div", id="genr").find("ul", class_="genre")

        if not daftar:
            return {"error": {"msg", "data kosong"}}

        result = {
            "manga_result": [],
            "semua_genre": [],
            "page_selanjutnya": False, 
            "page_sebelumnya": False
        }

        pages = soup.find("div", class_="pag-nav")

        if pages:
            result['page_selanjutnya'] = True if pages.find("a", class_="next") else False
            result['page_sebelumnya'] = True if pages.find("a", class_="prev") else False

        # scrap for manga
        for manga_search in daftar.find_all("div", class_="bge"):
            item1 = manga_search.find("div", class_="bgei")
            item2 = manga_search.find("div", class_="kan")
            chapters = item2.find_all("div", class_="new1")

            komik_item = {
                "title": item2.a.h3.text.replace('\t', '').replace('\n','').strip(),
                "url": self._fixUrl(item1.a['href']),
                "cover": self._fixImgSource(item1.a.img['data-src']),
                "info": item2.p.text.replace('\t', '').replace('\n','').strip(),
                "type": (item1.find("div", class_="tpe1_inf").text).replace('\n',' ').strip(),
                "chapter": {
                    "Awal": {
                        "title": chapters[0].a.find_all("span")[1].text,
                        "link": self._fixUrl(chapters[0].a['href'])
                    },
                    "Terbaru": {
                        "title": chapters[1].a.find_all("span")[1].text,
                        "link": self._fixUrl(chapters[1].a['href'])
                    }
                }
            }   

            result['manga_result'].append(komik_item)
        
        # scrap for genre
        for genre in genres.find_all("li"):
            # print(genre)
            result['semua_genre'].append({
                "title": genre.a.text,
                "url": self._fixUrl(genre.a['href'])
            })

        return result
        
    def _fixImgSource(self, link: str):
        return link.replace('i0.wp.com/', '').replace("i0.wp.com", '')

    def _isLink(self, link: str):
        link = link.strip()
        return link.startswith('http') or link.startswith('https')

if __name__ == "__main__":
    import sys
    manga = MangaScrapper()
    # manga.mangaInfo('https://komiku.id/manga/one-piece-indonesia/')
    a = manga.searchByGenre('isekai')
    print(a)
