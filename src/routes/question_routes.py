from flask import Blueprint, Response, request

from src.controllers.icontroller_question import IControllerQuestion
from src.controllers.controller_question import ControllerQuestion
from src.core.constraints import Methods
from src.core.wrappers.authenticate import authenticated
from src.core.wrappers.exception_handler import exception_handler


question_route = Blueprint('question_route', __name__, url_prefix='/question')
controller_question: IControllerQuestion = ControllerQuestion()


@exception_handler
@question_route.route("/", methods=[Methods.POST])
@authenticated
async def generate_questions() -> Response:
    return await controller_question.generate_questions(request)


@exception_handler
@question_route.route("/from-pdf", methods=[Methods.POST])
@authenticated
async def generate_question_from_pdf() -> Response:
    return await controller_question.generate_question_from_pdf(request)
