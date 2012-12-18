import urlparse
from datetime import datetime
from twisted.web.client import getPage
from twisted.web.http_headers import Headers
from phonon.client import Client


class TxClient(Client):
    """
    Client for sending data to Holodeck with Twisted's `getPage`.
    """

    def send(self, api_key, samples, timestamp):
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
        })
        headers = {
            'Content-Type': ['application/octet-stream'],
        }
        url = urlparse.urljoin(self.server, '/api/store/')
        return getPage(url, headers=Headers(headers), postdata=data)
