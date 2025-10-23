from flask import Flask
from flask_cors import CORS

from src.core.constraints import Environ, Methods
from src.core.origins import get_origins
from src.routes.prompt_routes import prompt_route

app = Flask(Environ.APP_NAME)

origins = get_origins()

CORS(app, origins=origins, methods=[
    Methods.POST
])

app.register_blueprint(prompt_route)


if __name__ == '__main__':
    app.run(debug=True, port=Environ.PORT, host=Environ.HOST)
