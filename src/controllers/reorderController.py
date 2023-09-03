
from flask import jsonify, request
from src.services.palm_api_Service import get_solutions


def set_response_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
    return response


def getSolutions(query):
    try:
        pdf_content = request.get_data()
        solutions = get_solutions(pdf_content, query)
        structuredData = jsonify(data=solutions)
        response = set_response_headers(structuredData)
        return response, 200

    except Exception as e:
        return jsonify(error=str(e)), 500
