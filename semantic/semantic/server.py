from flask import Flask
from flask_restful import Api
from semantic.endpoints import FaissSearchIndex, FaissRangeSearchIndex

app = Flask(__name__)
api = Api(app)

api.add_resource(FaissSearchIndex, "/sem_search")
api.add_resource(FaissRangeSearchIndex, "/sem_range_search")
