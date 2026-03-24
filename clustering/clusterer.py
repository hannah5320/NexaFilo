# clustering/clusterer.py

import hdbscan
import numpy as np
from config import MIN_CLUSTER_SIZE, MIN_SAMPLES


class Clusterer:
    def __init__(self):
        self.clusterer = hdbscan.HDBSCAN(
            min_cluster_size=MIN_CLUSTER_SIZE,
            min_samples=MIN_SAMPLES,
            metric="euclidean",
            prediction_data=True
        )

    def fit(self, embeddings):
        # Normalize embeddings (critical for cosine equivalence)
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        normalized_embeddings = embeddings / (norms + 1e-10)

        labels = self.clusterer.fit_predict(normalized_embeddings)
        probabilities = self.clusterer.probabilities_

        return labels, probabilities
