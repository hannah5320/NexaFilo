import json
import os
from .folder_manager import create_cluster_folder
from .file_mover import move_file_safe


def apply_clusters(base_path):

    from config import FINAL_EXPORT_PATH

    cluster_file = FINAL_EXPORT_PATH

    if not os.path.exists(cluster_file):
        print("final_clusters.json not found")
        return

    with open(cluster_file, "r") as f:
        clusters = json.load(f)

    for cluster_name, files in clusters.items():

        print(f"\nCreating folder for cluster: {cluster_name}")

        cluster_path = create_cluster_folder(base_path, cluster_name)

        for file_path in files:
            move_file_safe(base_path, file_path, cluster_path)

    print("\nOrganization Complete.")