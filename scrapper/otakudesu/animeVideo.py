import re, pprint

from anime_download.otakudesu import Otakudesu
from anime_download.bypasser import Bypass
from constant import OTAKUDESU_LINK

"""
mendapatkan link download yang ada di key
"""
def searchDownload(downloadList: dict, key: str)->  str:
    downloadValue = None

    for download in downloadList['value']:
        if download['key'].lower() == key.lower():
            downloadValue = download['value']

    if not downloadValue:
        keys = [x['key'] for x in downloadList['value']]
        raise Exception(key + " tidak ada didalam list silahkan cek dibawah\n" + "\n".join(keys) + '\n')


    return downloadValue

"""
mendapaktkan link download dari quality
"""
def searchQuality(downloadList: list[dict[str]], quality)-> dict:
    result = None

    for download in downloadList:
        download['key'] = download['key'].lower()
        # print(download, "semua download", "\n\n")
        if download['key'].find(quality) != -1:
            if download['key'].find('mkv') == -1: 
                result = download

    if not result:
        raise Exception("Quality tidak ditemukan anjay")

    return result

class AnimeVideoFetch:
    def __init__(self, id):
        self.link = id
        # https://otakudesu.moe/kdgnk-episode-19-sub-indo
        id = id.replace(OTAKUDESU_LINK + "/", '')
        self.id = id

    def _getFormatMp4(self, web)-> list:
        if web == "otakudesu":
            link = Otakudesu()
        elif web == "nekonime":
            print("sedang dikerjakan")
            # link = Nekonime()
            return
        
        webExtract = link.extract(self.id)

        # regex = re.compile(r"^(mp4|360|480|720)")

        result = []

        # print(pprint.pformat(webExtract), self.id)
        for download in webExtract['download']:
            for downloadValue in download['value']:
                # print(downloadValue)
                if downloadValue['key'].lower().find('mkv') == -1:
                    # # 360
                    # if downloadValue['key'].lower().find('360p') != -1:
                    #     if downloadValue['value'][0]['key'].lower().find('zippyshare') != -1:
                    #         zippyShare = downloadValue['value'][0]['value']
                    #         result['360p'] = lk21Bypass.bypass_zippyshare(zippyShare)
                    # # 480
                    # elif downloadValue['key'].lower().find('480p') != -1:
                    #     if downloadValue['value'][0]['key'].lower().find('zippyshare') != -1:
                    #         zippyShare = downloadValue['value'][0]['value']
                    #         result['480p'] = lk21Bypass.bypass_zippyshare(zippyShare)
                    # # 720
                    # elif downloadValue['key'].lower().find('720p') != -1:
                    #     if downloadValue['value'][0]['key'].lower().find('zippyshare') != -1:
                    #         zippyShare = downloadValue['value'][0]['value']
                    #         result['720p'] = lk21Bypass.bypass_zippyshare(zippyShare)


                    result.append(downloadValue)

        return result

    def get_360p(self, web, typevid: str = "mp4", downloadKey = "zippyshare"):
        QUALITY = '360p'
        typevid = typevid.lower()
        lk21Bypass = Bypass()

        if typevid == "mp4":
            mp4_video = self._getFormatMp4(web)
            q_360p = searchQuality(mp4_video, QUALITY)
            searchDL = searchDownload(q_360p, downloadKey)

            if downloadKey == "zippyshare":
                return lk21Bypass.bypass_zippyshare(searchDL)
            elif downloadKey == "racaty":
                return lk21Bypass.bypass_filesIm(searchDL.replace('.com', '.net'))
            elif downloadKey == "filesim":
                return lk21Bypass.bypass_filesIm(searchDL)

    def get_480p(self, web, typevid: str = "mp4", downloadKey = "zippyshare"):
        QUALITY = '480p'
        typevid = typevid.lower()
        lk21Bypass = Bypass()

        if typevid == "mp4":
            mp4_video = self._getFormatMp4(web)
            q_480p = searchQuality(mp4_video, QUALITY)
            searchDL = searchDownload(q_480p, downloadKey)

            if downloadKey == "zippyshare":
                return lk21Bypass.bypass_zippyshare(searchDL)
            elif downloadKey == "racaty":
                return lk21Bypass.bypass_filesIm(searchDL.replace('.com', '.net'))
            elif downloadKey == "filesim":
                return lk21Bypass.bypass_filesIm(searchDL)

    def get_720p(self, web, typevid: str = "mp4", downloadKey = "zippyshare"):
        QUALITY = '720p'
        typevid = typevid.lower()
        lk21Bypass = Bypass()
        downloadKey = downloadKey.lower()

        if typevid == "mp4":
            mp4_video = self._getFormatMp4(web)
            q_720p = searchQuality(mp4_video, QUALITY)
            searchDL = searchDownload(q_720p, downloadKey)

            if downloadKey == "zippyshare":
                return lk21Bypass.bypass_zippyshare(searchDL)
            elif downloadKey == "racaty":
                return lk21Bypass.bypass_filesIm(searchDL.replace('.com', '.net'))
            elif downloadKey == "filesim":
                return lk21Bypass.bypass_filesIm(searchDL)
            # return mp4_video
            
 
    def getFormatMkv(self):
        otaku = Otakudesu()
        otakuExtract = otaku.extract(self.id)
        lk21Bypass = Bypass()

        result = {
            "480p": None,
            "720p": None,
            "1080p": None,
            "allmkvdownload": [] 
        }

        for download in otakuExtract['download']:
            for downloadValue in download['value']:
                if downloadValue['key'].lower().find('mkv') != -1:
                    # 480
                    if downloadValue['key'].lower().find('480p') != -1:
                        if downloadValue['value'][0]['key'].lower().find('zippyshare') != -1:
                            zippyShare = downloadValue['value'][0]['value']
                            result['480p'] = lk21Bypass.bypass_zippyshare(zippyShare)
                    # 720
                    elif downloadValue['key'].lower().find('720p') != -1:
                        if downloadValue['value'][0]['key'].lower().find('zippyshare') != -1:
                            zippyShare = downloadValue['value'][0]['value']
                            result['720p'] = lk21Bypass.bypass_zippyshare(zippyShare)
                    # 1080
                    elif downloadValue['key'].lower().find('1080p') != -1:
                        if downloadValue['value'][0]['key'].lower().find('zippyshare') != -1:
                            zippyShare = downloadValue['value'][0]['value']
                            result['1080p'] = lk21Bypass.bypass_zippyshare(zippyShare)

                    result['allmkvdownload'].append(downloadValue)

        return result

if __name__ == '__main__':
    import time
    anime = AnimeVideoFetch(
        'https://otakudesu.vip/iruma-kun-s2-episode-7-sub-indo/'
    )

    start = time.time()
    # a = anime.get_720p()
    end = time.time()
    print("Time exe v1: " + str(end - start))
    # print(a)


# .getVideo('https://uservideo.xyz/file/nanime.biz.isekai.maou.to.shoukan.shoujo.no.dorei.majutsu.e07.1080p.sub.indo.mp4')