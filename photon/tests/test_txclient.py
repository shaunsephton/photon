"""Tests for photon.txclient."""

from datetime import datetime

from twisted.trial.unittest import TestCase
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, maybeDeferred
from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.resource import Resource
from twisted.web import http

from photon.txclient import TxClient


class TestException(Exception):
    """
    Used to flag exceptions that DummyServer should retreat
    as internal server errors.
    """


class DummyServerResource(Resource):

    isLeaf = True

    def __init__(self):
        self.request_handler = self.no_handler

    def no_handler(self):
        raise RuntimeError("No handler set.")

    def set_request_handler(self, f):
        self.request_handler = f

    def render(self, request):
        request.setHeader('Content-Type', 'text/plain')
        d = maybeDeferred(self.request_handler, request)

        def on_success(data):
            request.setResponseCode(http.OK)
            request.write(data)
            request.finish()

        def on_error(failure):
            request.setResponseCode(http.INTERNAL_SERVER_ERROR)
            request.write(str(failure))
            request.finish()
            if not failure.check(TestException):
                return failure

        d.addCallbacks(on_success, on_error)

        return NOT_DONE_YET


class TestTxClient(TestCase):

    @inlineCallbacks
    def setUp(self):
        self.root = DummyServerResource()
        site_factory = Site(self.root)
        self.webserver = yield reactor.listenTCP(0, site_factory)
        addr = self.webserver.getHost()
        self.txclient = TxClient("http://%s:%s/" % (addr.host, addr.port))

    @inlineCallbacks
    def tearDown(self):
        yield self.webserver.loseConnection()

    @inlineCallbacks
    def test_send(self):
        samples = [
            ["Line 1", 101],
            ["Line 2", 102],
        ]
        now = datetime.now()

        def check_request(request):
            self.assertEqual(request.uri, '/api/store/')
            self.assertEqual(request.method, 'POST')
            self.assertEqual(request.headers['content-type'], 'text/plain')
            raw_data = request.content.read()
            data = self.txclient.decode(raw_data)
            self.assertEqual(data['timestamp'],
                             datetime.strftime(now, '%Y-%m-%d %H:%M:%S'))
            self.assertEqual(data['api_key'], '1')
            self.assertEqual(data['samples'], samples)
            return "ok"

        self.root.set_request_handler(check_request)
        response = yield self.txclient.send(api_key="1", samples=samples,
                                            timestamp=now)
        self.assertEqual(response, "ok")
