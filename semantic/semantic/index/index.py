import os
import faiss
import numpy as np
import pickle
from semantic.config import CONFIG
from semantic.logging import logger
from semantic.embeddings import calculate_embedding


class FAISSIndex:
    """Class that represents FAISS index"""

    def __init__(self):
        try:
            self.index = faiss.read_index(
                os.getenv("FAISS_INDEX_PATH"),
            )
            with open(
                os.getenv("FAISS_UUIDS_PATH"),
                "rb",
            ) as f_in:
                cached_data = pickle.load(f_in)
                self.uuids = cached_data["uuids"]
        except IOError:
            logger.error(
                "Couldn't instantiate the FAISS index",
                exc_info=True,
            )

    def search(self, query):
        """Searches FAISS index

        Args:
            query (str): Query text

        Returns:
            list: List of found ids

        """
        query_embeddings = self._prepare_query_embeddings(query)
        distance, ids = self.index.search(
            query_embeddings,
            CONFIG["faiss_top_hits"],
        )
        result = []
        for score, index_id in zip(distance.tolist()[0], ids.tolist()[0]):
            result.append(
                {
                    "score": score,
                    "index_id": index_id,
                    "uuid": self.uuids[index_id],
                }
            )
        return result

    def range_search(self, query):
        """Searches FAISS index

        Args:
            query (str): Query text

        Returns:
            list: List of found ids

        """
        query_embeddings = self._prepare_query_embeddings(query)
        _, distance, ids = self.index.range_search(
            query_embeddings,
            CONFIG["faiss_score_limit"],
        )
        result = []
        for score, index_id in zip(distance.tolist(), ids.tolist()):
            result.append(
                {
                    "score": score,
                    "index_id": index_id,
                    "uuid": self.uuids[index_id],
                }
            )
        return result

    def _prepare_query_embeddings(self, query):
        """Prepares query embeddings

        Args:
            query (str): Query text

        Returns:
            obj: Numpy vector

        """
        query_embeddings = calculate_embedding(query)
        query_embeddings = query_embeddings / np.linalg.norm(query_embeddings)
        return np.expand_dims(
            query_embeddings,
            axis=0,
        )


faiss_index = FAISSIndex()
