from typing import List

from src.core.constraints import Environ


def get_origins() -> List[str]:
    with open(Environ.CORS_FILE_NAME, "r") as file:
        data = file.readlines()
        data = (link[:-1] for link in data)
    return [link for link in data]
