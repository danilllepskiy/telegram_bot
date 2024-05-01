import os

from dotenv import load_dotenv
from pydantic import SecretStr, BaseSettings


load_dotenv()


class Settings(BaseSettings):
    api_key: SecretStr = os.getenv("SITE_API", None)
    bot_token: SecretStr = os.getenv("BOT_TOKEN", None)
