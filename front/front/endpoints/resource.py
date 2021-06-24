import flask_restful
from .authentication import require_appkey


class Resource(flask_restful.Resource):
    """Custom Resource that has require_appkey decorator"""

    method_decorators = [require_appkey]
