from typing import Any, Dict, Optional

from farcaster.models import *

FARCASTER_API_BASE_URL = "https://api.farcaster.xyz/v2/"


class ConfigurationParams(BaseModel):
    username: NoneStr
    password: NoneStr
    base_path: str = FARCASTER_API_BASE_URL
    base_options: Optional[Dict[Any, Any]]


class Configuration(BaseModel):
    params: Optional[ConfigurationParams]

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.params = ConfigurationParams(**data)
