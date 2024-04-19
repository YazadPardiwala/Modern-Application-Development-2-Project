import json
from werkzeug.exceptions import HTTPException

from flask import make_response

class BusinessValidationError(HTTPException):
    def __init__(self, status_code, error_message):
        message = {"error_message": error_message}
        self.response = make_response(json.dumps(message), status_code)