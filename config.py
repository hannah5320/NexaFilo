import os

# Embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Clustering parameters (loosened for small datasets)
MIN_CLUSTER_SIZE = 2
MIN_SAMPLES = 1

# Confidence threshold for cluster acceptance
CONFIDENCE_THRESHOLD = 0.3

# Database
DATABASE_PATH = "feedback.db"

# Storage paths
EMBEDDINGS_PATH = "storage/embeddings.npy"
FILE_INDEX_PATH = "storage/file_index.json"
CLUSTERS_PATH = "storage/clusters.json"
FINAL_EXPORT_PATH = "exports/final_clusters.json"

# ML model
MODEL_PATH = "models/similarity_model.pkl"

# Ensure directories exist
os.makedirs("storage", exist_ok=True)
os.makedirs("exports", exist_ok=True)
os.makedirs("models", exist_ok=True)
