from flask import request, Response
from flask.blueprints import Blueprint

from src.controllers.controller_prompt import ControllerPrompt
from src.controllers.icontroller_prompt import IControllerPrompt
from src.core.constraints import Methods

prompt_route = Blueprint('prompt_routes', __name__, url_prefix='/prompt-questions')

controller_prompt: IControllerPrompt = ControllerPrompt()


@prompt_route.route("/", methods=[Methods.POST])
async def prompt_questions() -> Response:
    return await controller_prompt.generate_questions(request)


@prompt_route.route("/study-tip", methods=[Methods.POST])
async def prompt_study_tip() -> Response:
    return await controller_prompt.generate_study_tips(request)
