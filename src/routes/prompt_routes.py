from flask import Request, Response
from flask.blueprints import Blueprint

from src.controllers.controller_prompt import ControllerPrompt
from src.controllers.icontroller_prompt import IControllerPrompt
from src.core.constraints import Headers, Methods

prompt_route = Blueprint('prompt_routes', __name__, url_prefix='/prompt-questions')

controller_prompt: IControllerPrompt = ControllerPrompt()


@prompt_route.route("/", methods=[Methods.POST], headers=Headers.JSON_ONE)
async def prompt_questions(request: Request) -> Response:
    return await controller_prompt.generate_questions(request)
