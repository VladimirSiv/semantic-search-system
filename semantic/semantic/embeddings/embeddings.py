import numpy as np
from semantic.config import CONFIG
from semantic.model import model


def _get_chunks(text, length=200, overlap=50):
    """Splits text into chunks

    Args:
        text (str): Text
        length (int, optional): Chunk length. Defaults to 200
        overlap (int, optional): Chunk overlap. Defaults to 50

    Return:
        list: Text chunks

    """
    l_total = []
    l_partial = []
    text_split = text.split()
    n_words = len(text_split)
    splits = n_words // (length - overlap) + 1
    if n_words % (length - overlap) == 0:
        splits = splits - 1
    if splits == 0:
        splits = 1
    for split in range(splits):
        if split == 0:
            l_partial = text_split[:length]
        else:
            l_partial = text_split[
                split * (length - overlap) : split * (length - overlap) + length
            ]
        l_final = " ".join(l_partial)
        if split == splits - 1:
            if len(l_partial) < 0.75 * length and splits != 1:
                continue
        l_total.append(l_final)
    return l_total


def calculate_embedding(text):
    """Calculates embeddings of a text

    Args:
        text (str): Text

    Return:
        numpy.array: Embeddings vector

    Note:
        This function breaks a long text into several chunks,
        calculates embedding for each chunk and then finds a mean
        embedding. That's the vector representation of the text which
        we will use for FAISS.

    """
    chunks = _get_chunks(text)
    embeddings = np.empty(
        shape=[
            len(chunks),
            CONFIG["embedding_size"],
        ],
        dtype="float32",
    )
    for index, chunk in enumerate(chunks):
        chunk_embedding = model.encode(
            chunk,
            convert_to_numpy=True,
        )
        embeddings[index:] = chunk_embedding
    mean = embeddings.mean(axis=0)
    mean_normalized = mean / np.linalg.norm(mean)
    return mean_normalized
