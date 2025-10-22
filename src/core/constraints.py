from os import environ

from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass
class Environ:
    GEMINI_API_KEY = environ.get("GEMINI_API_KEY") or "gemini-api-key"
