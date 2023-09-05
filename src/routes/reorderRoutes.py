from flask import Blueprint
from src.controllers.reorderController import getSolutions

reorderBlueprint = Blueprint('blueprintt', __name__)

# suggesting solutions by reading PDF file

reorderBlueprint.route('/getSolutions/<query>', methods=['POST'])(getSolutions)
