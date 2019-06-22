import urllib.request

from socket import timeout


def get_youtube_metadata(url):
    metadata_api = 'http://www.youtube.com/oembed?url={}&format=json'.format(url)
    try:
        response = urllib.request.urlopen(
            metadata_api, timeout=10
        ).read().decode('utf-8')
        return True, response
    except Exception as e:
        return False, {'message': str(e)}
