
import re
from .common import InfoExtractor
from ..utils import OnDemandPagedList


class StasyQIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?stasyq\.com/(r/[\w-]+/)?(?P<id>[0-9]+)'
    _TESTS = [{
        'url': 'https://www.stasyq.com/r/Katya-Killer/310',
        'md5': 'fcf1174d6baa4919c9522667d480d3ea',
        'info_dict': {
            'id': '310',
            'ext': 'mp4',
            'title': ' Katya Killer Video Release 310',
            'duration': 31.0,
            'upload_date': '20181209',
            'thumbnail': 'https://files.stasyq.com/files/images/galleries/563/medium/1536751489_horizontal.jpg',
            'view_count': int,
            'timestamp': 1544313600,
            'description': 'md5:42961dd53f072e3d87d20a216e623815',
        },
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        # info = self._html_search_regex(r'<script type="application/ld\+json">(.+?)</script>', webpage, 'title')
        # i = self._parse_json(info, url)

        i=self._search_json_ld(webpage, video_id)

        self.to_screen(i)
        i['id'] = video_id
        return i

class StasyQPlaylistIE(InfoExtractor):
    _VALID_URL = r'https?://www\.stasyq\.com/releases'
    _TESTS = [{
        'url': 'https://www.stasyq.com/releases',
        'info_dict': {
            'id': 'all1',
        },
        'playlist_mincount': 1500,
    }]

    def _real_extract(self, url):

        def fetch_page(page_num):
            page_num += 1
            page = self._download_webpage(
                f'https://www.stasyq.com/releases/{page_num}',f'releases/{page_num}',
                f'Downloading page {page_num}', tries=5, timeout=5)

            urls1 = re.findall(r'(?P<id>https?://(?:www\.)?stasyq\.com/r/[\w-]+/[0-9]+)', page)
            urls2 = re.findall(r'(?P<id>https?://(?:www\.)?stasyq\.com/[0-9]+)', page)
            urls = set(urls1).union(urls2)
            self.to_screen(f'Downloaded page {page_num} {len(page)} chars with {len(urls)} videos')
            for url in urls:
                self.write_debug(f'found url {url}')
                self.to_screen(f'found url {url}')
                yield self.url_result(url)

        return self.playlist_result(OnDemandPagedList(fetch_page, 15), 'all')

class StasyQBackstageIE(InfoExtractor):
    _VALID_URL = r'https?://www\.stasyq\.com/backstage-videos'
    _TESTS = [{
        'url': 'https://www.stasyq.com/backstage-videos',
        'info_dict': {
            'id': 'all1',
        },
        'playlist_mincount': 1500,
    }]

    def _real_extract(self, url):

        def fetch_page(page_num):
            page_num += 1
            page = self._download_webpage(
                f'https://www.stasyq.com/backstage-videos/{page_num}',f'backstage-videos/{page_num}',
                f'Downloading page {page_num}', tries=5, timeout=5)

            urls = re.findall(r'(?P<id>https?://(?:www\.)?stasyq\.com/storage/sqfiles/releases/[\w-]+/[\w-]+.mp4)', page)
            self.to_screen(f'Downloaded page {page_num} {len(page)} chars with {len(urls)} videos')
            for url in urls:
                self.to_screen(f'found url {url}')
                yield self.url_result(url)

        return self.playlist_result(OnDemandPagedList(fetch_page, 15), 'all')
