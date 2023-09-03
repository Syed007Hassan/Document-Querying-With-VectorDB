from flask import jsonify
from flask import jsonify, request
from src.services.palm_api_Service import palm_create_response, palm_chat_response, get_solutions
from src.services.reorderService import ReorderService
import PyPDF2
import os


def set_response_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
    return response


def getData():
    try:
        reorder_service = ReorderService()
        structured_data = reorder_service.get_reorder_data()
        response = jsonify(data=structured_data)
        response = set_response_headers(response)
        return response, 200
    except Exception as e:
        return jsonify(error=str(e)), 500


def getVendorData(itemCode):
    try:
        reorder_service = ReorderService()
        structured_data = reorder_service.get_vendor_data(itemCode)
        response = jsonify(data=structured_data)
        response = set_response_headers(response)
        return response, 200
    except Exception as e:
        return jsonify(error=str(e)), 500


def emailService(itemCode, vendorId, itemQuantity, costPrice):
    try:
        reorder_service = ReorderService()
        pdf_content = request.get_data()
        email_msg = reorder_service.send_email(
            itemCode, vendorId, itemQuantity, costPrice, pdf_content)
        structuredData = jsonify(data=email_msg)
        response = set_response_headers(structuredData)
        return response, 200

    except Exception as e:
        return jsonify(error=str(e)), 500


def getSolutions(query):
    try:
        pdf_content = request.get_data()
        solutions = get_solutions(pdf_content, query)
        structuredData = jsonify(data=solutions)
        response = set_response_headers(structuredData)
        return response, 200

    except Exception as e:
        return jsonify(error=str(e)), 500


def chatWithBARD(prompt):
    try:
        message = palm_chat_response(prompt)
        structuredData = jsonify(data=message)
        response = set_response_headers(structuredData)
        return response, 200
    except Exception as e:
        # Log the error
        # Return an error message to the user
        return "An error occurred while processing your request. Please try again later.", 500
