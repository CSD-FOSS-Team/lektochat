import pytest
import tempfile
from lektochat_server.lektochat_server import LektoServer

tempdb = tempfile.NamedTemporaryFile()
server = LektoServer(tempdb.name)
testclients = [['test4', '192.168.1.1'],
               ['test5', '2.3.5.199'],
               ['test6', '198.211.122.15']]


def test_newconnection():
    # Test IP checks
    assert server.newconnection("test1", "171.87.1") is False
    for i, client in enumerate(testclients):
        assert server.newconnection(client[0], client[1]) is True


def test_search():
    for i, client in enumerate(testclients):
        assert server.search(client[0]) == client[1]
    assert server.search('foobar') is None


def test_disconnection():
    for i, client in enumerate(testclients):
        assert server.disconnect(client[1]) is True
    assert server.disconnect('122.1.1.1') is None
