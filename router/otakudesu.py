from flask import Blueprint, request
from scrapper import FetchBeranda, AnimeFetch, AnimeVideoFetch, AnimeSearch
from constant import OTAKUDESU_LINK

otaku = Blueprint("otakudesu", __name__, url_prefix="/api")

@otaku.route("/otakudesu")
def otakudesu_home():
    page = request.args.get('page') or None
    return_type = request.args.get('type') or ""
    search = request.args.get("search")

    beranda = FetchBeranda()

    if search:
        sh = AnimeSearch(search).otakudesuSearch()

        return {"result":sh}

    if return_type == "ongoing":
        return {
            "ongoing": beranda.getAllOngoingAnime(page)
        }
    elif return_type == "complete":
        return {
            "complete": beranda.getCompleteAnime(page)
        }
    else:
        return {
            "ongoing": beranda.getAllOngoingAnime(page), 
            "complete": beranda.getCompleteAnime(page)
        }

@otaku.route("/otakudesu/anime/<details>")
def otakudesu_anime_details(details):
    fetch = AnimeFetch(f"{OTAKUDESU_LINK}/anime/{details}").getEpisodesOtakudesu()
    nAnime = []
    for anime in fetch["anime"]:
        nAnime.append({
            "animelink": anime["animelink"].replace(f"{OTAKUDESU_LINK}/", "").replace("/", ""), 
            "title": anime["title"]
        })

    fetch["anime"] = nAnime

    return fetch

@otaku.route("/otakudesu/<details>")
def otakudesu_details(details):
    video = AnimeVideoFetch(details)
    downloadKey = request.args.get("provider") or "zippyshare"

    try:
        return {
            "360p": video.get_360p("otakudesu", downloadKey=downloadKey),
            "480p": video.get_480p("otakudesu", downloadKey=downloadKey),
            "720p": video.get_720p("otakudesu", downloadKey=downloadKey),
        }
    except Exception as e:
        return ({"error": e.__str__()} ,404)
