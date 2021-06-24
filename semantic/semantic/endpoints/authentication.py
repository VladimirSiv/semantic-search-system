import os
from functools import wraps
from flask import request, abort

API_KEY = os.getenv("API_KEY")


def require_appkey(func):
    """Wrapper function that checks if APP_KEY is provided in request"""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        if request.args.get("key") and request.args.get("key") == API_KEY:
            return func(*args, **kwargs)
        abort(401)

    return decorated_function
