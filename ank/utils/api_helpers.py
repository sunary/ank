__author__ = 'sunary'


from datetime import timedelta
try:
    from flask import make_response, request, current_app, json
except ImportError:
    raise ImportError('flask not found')
from functools import update_wrapper


STATUS_CODE = {200: 'success',
               201: 'created',
               202: 'accepted',
               204: 'no_content',
               302: 'redirect',
               304: 'not_modified',
               400: 'bad_request',
               401: 'unauthorized',
               403: 'forbidden',
               404: 'not_found',
               405: 'method_not_allowed',
               409: 'conflict',
               412: 'precondition_failed',
               429: 'too_many_requests',
               500: 'internal_server_error',
               503: 'unavailable'}


def crossdomain(origin=None, methods=None, headers=None, max_age=21600,
                attach_to_all=True, automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


def get_options():
    options = {}

    if request.method == 'POST':
        get_json = request.get_json()

        if get_json:
            for k, v in get_json.items():
                options[k] = str(v)

        for field in request.form:
            options[field] = str(request.form.get(field))

    elif request.method == 'GET':
        for field in request.args:
            options[field] = str(request.args.get(field))

    return options


def failed(return_json={}, status_code=400, message=None):
    return_json['ok'] = False
    return_json['status_code'] = status_code
    return_json['message'] = message or STATUS_CODE.get(status_code)

    return json.jsonify(return_json)


def success(return_json={}, status_code=200, message=None):
    return_json['ok'] = True
    return_json['status_code'] = status_code
    return_json['message'] = message or STATUS_CODE.get(status_code)

    return json.jsonify(return_json)


def is_success(api_json):
    return api_json.get('ok') or api_json.get('status_code') == 200
