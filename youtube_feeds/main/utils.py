import json
import re
import urllib.request

from socket import timeout


YTB_RE = (r'http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)'
           '([\w\-\_]*)(&(amp;)?[\w\?=]*)?')


def get_youtube_metadata(url):
    vid = get_youtube_id(url)
    if not vid:
        return False, {'message': 'Invalid youtube url.'}
    metadata_api = 'http://www.youtube.com/oembed?url={}&format=json'.format(url)
    try:
        response = urllib.request.urlopen(
            metadata_api, timeout=10
        ).read().decode('utf-8')
        data = {'vid': vid, 'title': json.loads(response)['title']}
        return True, data
    except Exception as e:
        return False, {'message': str(e)}


def get_youtube_id(url):
    matches = re.search(YTB_RE, url)
    if matches:
        return matches.group(1)
    return None
