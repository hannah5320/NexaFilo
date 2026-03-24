# embedding/embedder.py

from typing import List, Union
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL


class Embedder:
    def __init__(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = SentenceTransformer(EMBEDDING_MODEL, device=device)

    def encode(self, texts: Union[str, List[str]]) -> np.ndarray:
        if isinstance(texts, str):
            texts = [texts]

        return self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=True
        )
