from typing import List

from flask import Flask

from src.core.constraints import Environ
from src.routes.prompt_routes import prompt_route

app = Flask(Environ.APP_NAME)


def origins() -> List[str]:
    with open(Environ.CORS_FILE_NAME, "r") as file:
        data = file.readlines()
        data = (link[:-1] for link in data)
    return [link for link in data]


app.register_blueprint(prompt_route)


if __name__ == '__main__':
    app.run(debug=True, port=Environ.PORT, host=Environ.HOST)
