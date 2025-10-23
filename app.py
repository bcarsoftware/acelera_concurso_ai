from flask import Flask

from src.core.constraints import Environ
from src.routes.prompt_routes import prompt_route

app = Flask(Environ.APP_NAME)


app.register_blueprint(prompt_route)


if __name__ == '__main__':
    app.run(debug=True, port=Environ.PORT, host=Environ.HOST)
