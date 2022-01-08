from youtubesearchpython import *


class Whatsapp_Functions(object):
    def __init__(self) -> None:
        super().__init__()

    def search_videos(self, search_term: str, limit: int = 5, language: str = 'US', region: str = 'US') -> str:
        videosSearch = CustomSearch(search_term, VideoUploadDateFilter.thisYear, limit=limit, language=language, region=region)
        return videosSearch.result()['result'][0]['link']