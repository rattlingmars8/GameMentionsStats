from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    game_data: str = "/game-mentions"
    steam_chart: str = "/steam-chart"


class ApiPrefix(BaseModel):
    value: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class RedditConfig(BaseModel):
    client_id: str
    client_secret: str
    user_agent: str


class FlaresolverConfig(BaseModel):
    proxy_url: str


class SteamConfig(BaseModel):
    search_url: str
    search_params: str
    followers_api_call: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_insensitive=True,
        env_nested_delimiter="__",
        env_prefix="FASTAPI__",
    )
    api_prefix: ApiPrefix = ApiPrefix()
    reddit: RedditConfig
    flaresolver: FlaresolverConfig
    steam: SteamConfig


settings = Settings()
