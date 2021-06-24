from flask import abort
from flask_restful import request
from marshmallow import Schema, fields, ValidationError
from marshmallow.utils import EXCLUDE
from front.semantic import SemanticSearch
from .resource import Resource

semantic_search = SemanticSearch()


class SemanticSearchSchema(Schema):
    """Defines Search Index endpoint request schema"""

    class Meta:
        unknown = EXCLUDE

    text = fields.Str(required=True)


semantic_search_schema = SemanticSearchSchema()


class SemanticSearchEndpoint(Resource):
    """Defines endpoint resource for index searching"""

    def post(self):
        """Initializes search query on semantic server"""
        try:
            params = semantic_search_schema.load(request.json)
            return semantic_search.simple_query(
                params["text"],
            )
        except ValidationError as val_err:
            abort(
                400,
                str(val_err),
            )


class SemanticRangeSearchEndpoint(Resource):
    """Defines endpoint resource for index range searching"""

    def post(self):
        """Initializes range search query on semantic server"""
        try:
            params = semantic_search_schema.load(request.json)
            return semantic_search.range_query(
                params["text"],
            )
        except ValidationError as val_err:
            abort(
                400,
                str(val_err),
            )
