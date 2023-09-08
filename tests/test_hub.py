from farcaster import Hub
from farcaster.hub.generated import request_response_pb2


def test_get_casts_by_fid(hub: Hub):
    request = request_response_pb2.FidRequest(fid=50)
    response = hub.client.GetCastsByFid(request)
    assert len(response.messages) > 266
