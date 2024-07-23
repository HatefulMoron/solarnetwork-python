from solarnetwork_python.client import Client


def test_nodes():
    client = Client("token", "secret")
    nodes = client.nodes()
    assert len(nodes) > 1
