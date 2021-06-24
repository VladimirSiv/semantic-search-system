from flask import abort
from flask_restful import request
from marshmallow import Schema, fields, ValidationError
from marshmallow.utils import EXCLUDE
from elasticsearch import ElasticsearchException
from front.elasticsearch import elastic_db
from front.logging import logger
from .resource import Resource


class ESSearchIndexSchema(Schema):
    """Defines Search Index endpoint request schema"""

    class Meta:
        unknown = EXCLUDE

    query = fields.Str(required=True)
    page = fields.Int(required=True)


es_search_schema = ESSearchIndexSchema()


class Search(Resource):
    """Defines endpoint resource for index searching"""

    def get(self):
        """Searches FAISS index using request query"""
        try:
            params = es_search_schema.load(request.args)
            if not elastic_db.is_connected():
                elastic_db.connect()
            result = elastic_db.search(
                query=params["query"],
                page=params["page"],
            )
            return result
        except ValidationError as val_err:
            abort(
                400,
                str(val_err),
            )
        except ElasticsearchException as es_err:
            logger.error(
                "Exception occured while getting articles with query: %s",
                params["query"],
                exc_info=True,
            )
            abort(
                500,
                str(es_err),
            )
