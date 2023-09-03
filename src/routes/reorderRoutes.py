from flask import Blueprint
from src.controllers.reorderController import chatWithBARD, getData, emailService, getVendorData, getSolutions

reorderBlueprint = Blueprint('blueprintt', __name__)

reorderBlueprint.route('/getData', methods=['GET'])(getData)
reorderBlueprint.route('/getVendorData/<itemCode>',
                       methods=['GET'])(getVendorData)
reorderBlueprint.route(
    '/emailService/<itemCode>/<vendorId>/<itemQuantity>/<costPrice>', methods=['POST'])(emailService)
reorderBlueprint.route('/chatWithBARD/<prompt>', methods=['GET'])(chatWithBARD)

# suggesting solutions by reading that PDF file

reorderBlueprint.route('/getSolutions/<query>', methods=['POST'])(getSolutions)
