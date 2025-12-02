from flask import request, Response
from flask.blueprints import Blueprint

from src.controllers.controller_prompt import ControllerPrompt
from src.controllers.icontroller_prompt import IControllerPrompt
from src.core.constraints import Methods
from src.core.wrappers.authenticate import authenticated
from src.core.wrappers.exception_handler import exception_handler

prompt_route = Blueprint('prompt_routes', __name__, url_prefix='/prompt-questions')

controller_prompt: IControllerPrompt = ControllerPrompt()


@exception_handler
@prompt_route.route("/study-tip", methods=[Methods.POST])
@authenticated
async def prompt_study_tip() -> Response:
    return await controller_prompt.generate_study_tips(request)
