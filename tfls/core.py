from tfl.client import Client
from tfl.api_token import ApiToken
import os


def verify():
    return 'tfls is working!'


def get_client():
    token = ApiToken(
        os.getenv("app_id"),
        os.getenv("app_key")
    )
    return Client(token)

