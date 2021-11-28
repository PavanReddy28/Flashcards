from flask import make_response
from werkzeug.exceptions import HTTPException

class NotFoundError(HTTPException):
    def __init__(self, status_code):
        self.response = make_response('', status_code)