# clustering/postprocess.py

import numpy as np
from config import CONFIDENCE_THRESHOLD


def assign_clusters(file_names, labels, probabilities, cluster_names):
    results = []

    for file_name, label, prob in zip(file_names, labels, probabilities):

        if label == -1 or prob < CONFIDENCE_THRESHOLD:
            cluster_name = "General"
        else:
            cluster_name = cluster_names.get(label, f"cluster_{label}")

        results.append({
            "file_name": file_name,
            "cluster": cluster_name,
            "confidence": float(prob)
        })

    return results
