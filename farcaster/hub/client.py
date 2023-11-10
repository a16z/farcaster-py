import os

import grpc
from dotenv import load_dotenv
from eth_account.signers.local import LocalAccount

from farcaster.config import *
from farcaster.hub.generated.rpc_pb2_grpc import HubServiceStub
from farcaster.models import *
from farcaster.utils.wallet import get_wallet

load_dotenv()


def get_insecure_client(address: str, use_async: bool = False) -> HubServiceStub:
    channel = (
        grpc.aio.insecure_channel(address)
        if use_async
        else grpc.insecure_channel(address)
    )
    return HubServiceStub(channel)


def get_ssl_client(address: str, use_async: bool = False) -> HubServiceStub:
    credentials = grpc.ssl_channel_credentials()
    channel = (
        grpc.aio.secure_channel(address, credentials=credentials)
        if use_async
        else grpc.secure_channel(address, credentials=credentials)
    )
    return HubServiceStub(channel)


def get_env_client(use_async: bool = False) -> HubServiceStub:
    return (
        get_ssl_client(os.environ["FARCASTER_HUB"], use_async)
        if os.getenv("FARCASTER_USE_SSL") == "true"
        else get_insecure_client(os.environ["FARCASTER_HUB"], use_async)
    )


def get_hub_client(
    hub_address: str, use_async: bool = False, use_ssl: bool = True
) -> HubServiceStub:
    return (
        get_ssl_client(hub_address, use_async)
        if use_ssl
        else get_insecure_client(hub_address, use_async)
    )


class Hub:
    config: ConfigurationParams
    wallet: Optional[LocalAccount]
    access_token: Optional[str]
    expires_at: Optional[PositiveInt]
    rotation_duration: PositiveInt
    client: HubServiceStub

    def __init__(
        self,
        hub_address: str = "nemes.farcaster.xyz:2283",
        use_ssl: bool = True,
        use_async: bool = False,
        mnemonic: Optional[str] = None,
        private_key: Optional[str] = None,
        access_token: Optional[str] = None,
        expires_at: Optional[PositiveInt] = None,
        rotation_duration: PositiveInt = 10,
        **data: Any,
    ):
        self.config = ConfigurationParams(**data)
        self.hub_address = hub_address
        self.use_ssl = use_ssl
        self.use_async = use_async
        self.wallet = get_wallet(mnemonic, private_key)
        self.access_token = access_token
        self.expires_at = expires_at
        self.rotation_duration = rotation_duration

        if not self.wallet:
            raise Exception("No wallet or access token provided")

        self.client = get_hub_client(
            hub_address=self.hub_address, use_ssl=self.use_ssl, use_async=self.use_async
        )

    def get_base_path(self):
        return self.config.base_path

    def get_base_options(self):
        return self.config.base_options
