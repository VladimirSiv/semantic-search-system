from flask import Flask
from flask_restful import Api
from front.endpoints import (
    Search,
    SemanticSearchEndpoint,
    SemanticRangeSearchEndpoint,
)

app = Flask(__name__)
api = Api(app)

api.add_resource(Search, "/search")
api.add_resource(SemanticSearchEndpoint, "/semantic_search")
api.add_resource(SemanticRangeSearchEndpoint, "/semantic_range_search")
