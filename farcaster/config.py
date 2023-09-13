from typing import Any, Dict, Optional

from farcaster.models import *

FARCASTER_API_BASE_URL = "https://api.warpcast.com/v2/"


class ConfigurationParams(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    base_path: str = FARCASTER_API_BASE_URL
    base_options: Optional[Dict[Any, Any]] = None


class Configuration(BaseModel):
    params: Optional[ConfigurationParams]

    def __init__(self, **data: Any):  # pragma: no cover
        super().__init__(**data)
        self.params = ConfigurationParams(**data)
