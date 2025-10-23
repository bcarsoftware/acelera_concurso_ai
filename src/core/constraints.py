from os import environ

from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass
class Environ:
    GEMINI_API_KEY = environ.get("GEMINI_API_KEY") or "gemini-api-key"
    SELECT_MODEL = environ.get("SELECT_MODEL") or "select-model"
    APP_NAME = environ.get("APP_NAME") or "app-name"


@dataclass
class GeminiModel:
    FLASH = "gemini-2.5-flash"
    FLASH_LIGHT = "gemini-2.5-flash-lite"
    PRO = "gemini-2.5-pro"


@dataclass
class HttpStatus:
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    UNPROCESSABLE_ENTITY = 422
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
    OK = 200


@dataclass
class Methods:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
