# libs/response.py

from flask import jsonify


def response_json_v2(data, status_code=200, message=""):
    response = {
        "data": data,
        "message": message
    }
    return jsonify(response), status_code


def response_json(code, msg=None, data=None):
    return {
        'code': code,
        'msg': msg,
        'data': data
    }
