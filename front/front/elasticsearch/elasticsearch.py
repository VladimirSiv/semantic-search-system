import os
from elasticsearch import Elasticsearch, ConnectionError
from front.logging import logger

ES_HOST = os.getenv("ES_HOST")
ES_PORT = os.getenv("ES_PORT")
ES_INDEX = os.getenv("ES_INDEX")
ES_PAG_SIZE = int(os.getenv("ES_PAG_SIZE"))


def _extract_articles(response):
    """Extracts article from ElasticSearch response

    Args:
        response (dict): ElasticSearch response data

    Returns:
        dict: Article

    """
    try:
        return [x["_source"] for x in response["hits"]["hits"]]
    except KeyError:
        logger.error(
            "Failed to extract article from ES's response",
            exc_info=True,
        )
        return {}


class ElasticDB:
    """Manages connection with ElasticSearch DB

    Attributes:
        es_client (obj): ElasticSearch client

    """

    def __init__(self):
        self.es_client = None

    def connect(self):
        """Establishes the connection with ElasticSearchDB"""
        try:
            logger.debug("Establishing a connection to the ElasticSearchDB")
            self.es_client = Elasticsearch(
                [
                    {
                        "host": ES_HOST,
                        "port": ES_PORT,
                    }
                ]
            )
        except ConnectionError:
            logger.error(
                "Failed to connect to the ElasticSearch DB",
                exc_info=True,
            )

    def is_connected(self):
        """Checks if connection to ElasticSearch is established

        Returns:
            bool: True if is established, otherwise False

        """
        if self.es_client and self.es_client.ping():
            return True
        return False

    @classmethod
    def create_uuid_query(cls, uuid):
        """Creates an uuid query body

        Args:
            uuid (str): Article uuid

        Returns:
            dict: Query body

        Note:
            This is used for bulk queries

        """
        return [
            {
                "index": ES_INDEX,
            },
            {
                "query": {
                    "match": {
                        "uuid.keyword": uuid,
                    },
                },
            },
        ]

    def get_article(self, uuid):
        """Gets an article based on uuid

        Args:
            uuid (str): Article uuid

        Returns:
            dict: Article

        """
        return _extract_articles(
            self.es_client.search(
                index=ES_INDEX,
                body={
                    "query": {
                        "match": {
                            "uuid.keyword": uuid,
                        }
                    }
                },
            )
        )

    def get_articles_bulk(self, uuids):
        """Gets articles in bulk based on uuids

        Args:
            uuids (list): List of uuids to fetch

        Returns:
            list: List of results

        """
        requests = []
        for uuid in uuids:
            requests.extend(self.create_uuid_query(uuid))
        response = self.es_client.msearch(body=requests)
        return [_extract_articles(x)[0] for x in response["responses"]]

    def search(self, query, page):
        """Searches ElasticDatabase

        Args:
            query (str): Query
            page (int): Offset

        Returns:
            list: List of articles

        """
        return _extract_articles(
            self.es_client.search(
                index=ES_INDEX,
                from_=(page - 1) * ES_PAG_SIZE,
                size=ES_PAG_SIZE,
                body={
                    "query": {
                        "match": {
                            "body": query,
                        },
                    },
                },
            )
        )


elastic_db = ElasticDB()
