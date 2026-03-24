# clustering/labeling.py

from collections import Counter
import re
import numpy as np

STOPWORDS = {
    "this", "that", "with", "from", "have",
    "were", "their", "about", "there",
    "which", "will", "shall", "into",
    "using", "used"
}


def extract_keywords(texts, top_k=3):
    words = []

    for text in texts:
        tokens = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
        tokens = [t for t in tokens if t not in STOPWORDS]
        words.extend(tokens)

    common = Counter(words).most_common(top_k)
    return [word for word, _ in common]


def generate_cluster_names(texts, labels):
    cluster_names = {}
    labels = np.array(labels)

    for label in np.unique(labels):
        if label == -1:
            continue

        cluster_texts = [
            texts[i] for i in range(len(texts))
            if labels[i] == label
        ]

        keywords = extract_keywords(cluster_texts)

        if keywords:
            name = "_".join(keywords)
        else:
            name = f"cluster_{label}"

        cluster_names[label] = name

    return cluster_names
