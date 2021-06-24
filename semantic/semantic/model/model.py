from sentence_transformers import SentenceTransformer
from semantic.config import CONFIG

model = SentenceTransformer(CONFIG["model_name"])
