import os
from typing import Union

from dotenv import load_dotenv


def load_environment_variables():
    if os.path.exists("../../.env"):
        load_dotenv("../../.env")


def env_variable(name: str, default=None) -> Union[str, bool]:
    value = os.getenv(name, default)
    if value and str(value).lower() == "false":
        return False
    if value and str(value).lower() == "true":
        return True
    return value


# === Database ===
POSTGRES_DB = env_variable('POSTGRES_DB')
POSTGRES_USER = env_variable('POSTGRES_USER')
POSTGRES_PASSWORD = env_variable('POSTGRES_PASSWORD')
POSTGRES_HOST = env_variable('POSTGRES_HOST')
POSTGRES_PORT = env_variable('POSTGRES_PORT')
