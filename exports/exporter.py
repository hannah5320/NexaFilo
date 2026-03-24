# exporter.py

import json
import csv
import os
from datetime import datetime


def _ensure_directory(path):
    os.makedirs(path, exist_ok=True)


def _flatten_clusters(cluster_dict):
    """
    Convert:
    {
        "ClusterA": ["file1", "file2"],
        "ClusterB": ["file3"]
    }

    Into:
    [
        {"cluster": "ClusterA", "file_name": "file1"},
        {"cluster": "ClusterA", "file_name": "file2"},
        {"cluster": "ClusterB", "file_name": "file3"}
    ]
    """
    flattened = []

    for cluster, files in cluster_dict.items():
        for file in files:
            flattened.append({
                "cluster": cluster,
                "file_name": file
            })

    return flattened


def export_to_json(results, output_dir="exports"):
    _ensure_directory(output_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(output_dir, f"clusters_{timestamp}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    return file_path


def export_to_csv(results, output_dir="exports"):
    _ensure_directory(output_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(output_dir, f"clusters_{timestamp}.csv")

    flattened = _flatten_clusters(results)

    if not flattened:
        return None

    keys = flattened[0].keys()

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(flattened)

    return file_path