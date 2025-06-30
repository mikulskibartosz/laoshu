from dataclasses import dataclass
from typing import Optional
from .envs import read_env_vars


@dataclass
class Config:
    scrapingant_api_key: Optional[str]
    openai_api_key: Optional[str]


def load_config() -> Config:
    vars = read_env_vars()
    return Config(
        scrapingant_api_key=vars.get("SCRAPINGANT_API_KEY"),
        openai_api_key=vars.get("OPENAI_API_KEY"),
    )
