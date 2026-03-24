import os

def create_cluster_folder(base_path, cluster_name):
    cluster_path = os.path.join(base_path, cluster_name)
    os.makedirs(cluster_path, exist_ok=True)
    return cluster_path