"""Phiphi types."""
from typing import Literal

PhiphiJobType = Literal["gather", "gather_delete", "classify", "tabulate"]
SocialPlatformType = Literal["facebook", "instagram", "tiktok", "x-twitter"]
MessageDataSourceType = Literal["apify"]
MessageDataType = Literal["post", "comment"]
