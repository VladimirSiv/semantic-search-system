from flask import abort
from flask_restful import request
from marshmallow import Schema, fields
from marshmallow.utils import EXCLUDE
from semantic.index import faiss_index
from .resource import Resource


class FaissSearchIndexSchema(Schema):
    """Defines Search Index endpoint request schema"""

    class Meta:
        unknown = EXCLUDE

    text = fields.Str(required=True)


faiss_search_schema = FaissSearchIndexSchema()


class FaissSearchIndex(Resource):
    """Defines endpoint resource for index searching"""

    def post(self):
        """Searches FAISS index"""
        errors = faiss_search_schema.validate(request.json)
        if errors:
            abort(400, str(errors))
        query = request.json["text"]
        result = faiss_index.search(query)
        if not result:
            return {}
        return result


class FaissRangeSearchIndex(Resource):
    """Defines endpoint resource for index range searching"""

    def post(self):
        """Searches FAISS index"""
        errors = faiss_search_schema.validate(request.json)
        if errors:
            abort(400, str(errors))
        query = request.json["text"]
        result = faiss_index.range_search(query)
        if not result:
            return {}
        return result