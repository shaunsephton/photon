import base64
from datetime import datetime
import json
import urllib2
import urlparse

class Client(object):
    """
    Some of this code was stolen from Raven/Sentry.
    """
    def __init__(self, server):
        self.server = server

    def send(self, api_key, samples, timestamp, interval):
        """
        Sends encoded data via HTTP.
        """
        # Samples should be iterable in iterable but not string.
        if isinstance(samples[0], basestring):
            samples = (samples,)
        data = self.encode({
            'api_key': api_key,
            'samples': samples,
            'timestamp': datetime.strftime(timestamp, '%Y-%m-%d %H:%M:%S'),
            'interval': interval,
        })
        headers = {
            'Content-Type': 'application/octet-stream',
        }
        url = urlparse.urljoin(self.server, '/api/store/')
        req = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(req, data).read()
        return response

    def encode(self, data):
        """
        Serializes ``data`` into a raw string.
        """
        return base64.b64encode(json.dumps(data).encode('zlib'))

    def decode(self, data):
        """
        Unserializes a string, ``data``.
        """
        return json.loads(base64.b64decode(data).decode('zlib'))
