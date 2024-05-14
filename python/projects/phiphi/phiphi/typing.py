"""Phiphi types."""
from typing import Literal

PhiphiJobType = Literal["gather", "classify", "tabulate"]
SocialPlatformType = Literal["facebook", "instagram", "tiktok", "x-twitter"]
MessageDataSourceType = Literal["apify"]
MessageDataType = Literal["post", "comment"]
