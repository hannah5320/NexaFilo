import os
import json
import numpy as np

from extraction.extractor import extract_text
from embedding.embedder import Embedder
from clustering.clusterer import Clusterer
from clustering.labeling import generate_cluster_names
from clustering.postprocess import assign_clusters
from feedback.database import init_db
from feedback.feedback_manager import collect_feedback
from feedback.learner import SimilarityLearner
from extraction.media_classifier import MediaClassifier
from os_integrator.apply_clusters import apply_clusters

from config import (
    EMBEDDINGS_PATH,
    CLUSTERS_PATH,
    FINAL_EXPORT_PATH
)


def load_files(folder, media_classifier):

    doc_texts = []
    doc_paths = []
    media_paths = []

    for file in os.listdir(folder):

        path = os.path.join(folder, file)

        if not os.path.isfile(path):
            continue

        if media_classifier.is_media(path):
            media_paths.append(path)

        else:
            text = extract_text(path)

            if text and text.strip():
                doc_texts.append(text)
                doc_paths.append(path)

    return doc_texts, doc_paths, media_paths


def main(folder):

    init_db()

    embedder = Embedder()
    media_classifier = MediaClassifier(embedder)

    texts, file_paths, media_paths = load_files(folder, media_classifier)

    if not texts and not media_paths:
        print("No valid files found.")
        return

    final_clusters = {}
    document_clusters = {}

    # ==========================================================
    # DOCUMENT CLUSTERING
    # ==========================================================

    if texts:

        embeddings = embedder.encode(texts)

        np.save(EMBEDDINGS_PATH, embeddings)

        clusterer = Clusterer()

        labels, probabilities = clusterer.fit(embeddings)

        print("Labels:", labels)
        print("Probabilities:", probabilities)

        cluster_names = generate_cluster_names(texts, labels)

        assignments = assign_clusters(
            file_paths,
            labels,
            probabilities,
            cluster_names
        )

        for item in assignments:

            cluster_name = item["cluster"]

            document_clusters.setdefault(cluster_name, []).append(
                os.path.basename(item["file_name"])
            )

        with open(CLUSTERS_PATH, "w") as f:
            json.dump(document_clusters, f, indent=4)

        final_clusters.update(document_clusters)

        # ======================================================
        # FEEDBACK + LEARNING
        # ======================================================

        learner = SimilarityLearner()

        model_loaded = learner.load_model()

        for cluster_name, files in document_clusters.items():

            if cluster_name == "General":
                continue

            print(f"\nCluster: {cluster_name}")
            print(f"Files: {len(files)}")

            cluster_size = len(files)

            similarity_scores = np.random.rand(cluster_size)

            avg_similarity = float(np.mean(similarity_scores))

            similarity_std = float(np.std(similarity_scores))

            if model_loaded:

                features = np.array([
                    [avg_similarity, cluster_size, similarity_std]
                ])

                probability = learner.predict_proba(features)[0][1]

                print(f"Model suggested acceptance probability: {probability:.3f}")

            collect_feedback(
                cluster_name,
                avg_similarity,
                cluster_size,
                similarity_std
            )

        learner.train()

    # ==========================================================
    # MEDIA CLASSIFICATION
    # ==========================================================

    if media_paths:

        print("\nProcessing Media Files...")

        for media_file in media_paths:

            print(f"\nMedia: {os.path.basename(media_file)}")

            category = media_classifier.classify(media_file)

            final_clusters.setdefault(category, []).append(
                os.path.basename(media_file)
            )

    # ==========================================================
    # FINAL EXPORT
    # ==========================================================

    with open(FINAL_EXPORT_PATH, "w") as f:
        json.dump(final_clusters, f, indent=4)

    print("\nCluster data exported.")

    # ==========================================================
    # APPLY CLUSTERS TO FILESYSTEM
    # ==========================================================

    print("\nApplying AI organization to filesystem...")

    apply_clusters(folder)

    print("\nPipeline completed successfully.")


if __name__ == "__main__":

    import sys

    if len(sys.argv) < 2:
        print("Please provide folder path.")
        sys.exit(1)

    folder_path = sys.argv[1]

    main(folder_path)