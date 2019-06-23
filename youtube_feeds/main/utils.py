import json
import re
import urllib.request

from socket import timeout


YTB_RE = (r'http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)'
           '([\w\-\_]*)(&(amp;)?[\w\?=]*)?')


def _get_as_json(url):
    res_data = urllib.request.urlopen(url, timeout=10).read().decode('utf-8')
    return json.loads(res_data)

def get_youtube_metadata(url):
    vid = get_youtube_id(url)
    if not vid:
        return False, {'message': 'Invalid youtube url.'}
    metadata_api = 'http://www.youtube.com/oembed?url={}&format=json'.format(url)
    try:
        json_data = _get_as_json(metadata_api)
        data = {
            'vid': vid,
            'title': json_data['title'],
            'author_name': json_data['author_name'],
            'author_url': json_data['author_url'],
        }
        return True, data
    except Exception as e:
        return False, {'message': str(e)}

def get_youtube_id(url):
    matches = re.search(YTB_RE, url)
    if matches:
        return matches.group(1)
    return None
