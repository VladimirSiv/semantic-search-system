import os
from flask import abort
from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError, Timeout
from urllib3.util.retry import Retry
from elasticsearch.exceptions import ElasticsearchException
from front.elasticsearch import elastic_db
from front.logging import logger

SEMANTIC_SERVER_PROTOCOL = os.getenv("SEMANTIC_SERVER_PROTOCOL")
SEMANTIC_SERVER_HOST = os.getenv("SEMANTIC_SERVER_HOST")
SEMANTIC_SERVER_PORT = os.getenv("SEMANTIC_SERVER_PORT")
SEMANTIC_SERVER_API_KEY = os.getenv("SEMANTIC_SERVER_API_KEY")


class SemanticSearch:
    """Class that requests to semantic search server

    Attributes:
        client (obj): Session object

    """

    def __init__(self):
        self.client = Session()
        self.client.mount(
            SEMANTIC_SERVER_PROTOCOL,
            HTTPAdapter(
                max_retries=Retry(
                    total=2,
                    backoff_factor=1,
                    status_forcelist=[
                        500,
                        502,
                        503,
                        504,
                        521,
                    ],
                )
            ),
        )

    def simple_query(self, text):
        """Processes query text using semantic server simple query

        Args:
            text (str): Query text

        Returns:
            dict: Result

        """
        return self._query(text, "/sem_search")

    def range_query(self, text):
        """Processes query text using semantic server range query

        Args:
            text (str): Query text

        Returns:
            dict: Result

        """
        return self._query(text, "/sem_range_search")

    def _query(self, text, endpoint):
        """First queries semantic server using range option to get article
        uuids then fetches those articles from elasticsearch, combines them
        in a single json that contains cosine scores i.e. semantic scores
        and article data

        Args:
            text (str): Query text
            endpoint (str): Semantic server endpoint

        Returns:
            dict: Articles with cosine scores

        """
        try:
            sem_result = self.client.post(
                SEMANTIC_SERVER_PROTOCOL
                + SEMANTIC_SERVER_HOST
                + ":"
                + SEMANTIC_SERVER_PORT
                + endpoint,
                params={
                    "key": SEMANTIC_SERVER_API_KEY,
                },
                json={
                    "text": text,
                },
            )
            sem_data = sem_result.json()
            if not sem_data:
                return {}
            uuids = [x["uuid"] for x in sem_data]
            if not elastic_db.is_connected():
                elastic_db.connect()
            el_result = elastic_db.get_articles_bulk(uuids)
            for s_res, e_res in zip(sem_data, el_result):
                s_res["article"] = e_res
            return sem_data
        except HTTPError:
            logger.error(
                "Semantic Search HttpError",
                exc_info=True,
            )
            abort(
                500,
                {
                    "message": "An error occured while handling your request",
                },
            )
        except Timeout:
            logger.error(
                "Semantic Search Timeout Error",
                exc_info=True,
            )
            abort(
                500,
                {
                    "message": (
                        "Services timed out, please try again in couple of minutes"
                    ),
                },
            )
        except ElasticsearchException:
            logger.error(
                "Semantic Search ElasticSearch Error",
                exc_info=True,
            )
            abort(
                500,
                {
                    "message": "An error occured while handling your request",
                },
            )
