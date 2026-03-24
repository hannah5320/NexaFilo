import os
import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression
from feedback.database import fetch_feedback
from config import MODEL_PATH


class SimilarityLearner:

    def __init__(self):
        self.model = None

    # -------------------------
    # Explicit Model Loader
    # -------------------------
    def load_model(self):
        if os.path.exists(MODEL_PATH):
            self.model = joblib.load(MODEL_PATH)
            print("Loaded trained feedback model.")
            return True
        else:
            print("No trained model found. Running in manual mode.")
            return False

    # -------------------------
    # Train Model
    # -------------------------
    def train(self):
        data = fetch_feedback()
        print("Feedback samples:", len(data))

        if len(data) < 10:
            print("Not enough feedback to train (minimum 10).")
            return

        X = np.array([
            [row[0], row[1], row[2]]  # avg_similarity, cluster_size, similarity_std
            for row in data
        ])

        y = np.array([row[3] for row in data])

        model = LogisticRegression()
        model.fit(X, y)

        joblib.dump(model, MODEL_PATH)
        self.model = model

        print("Feedback model trained successfully.")

    # -------------------------
    # Probability Prediction
    # -------------------------
    def predict_proba(self, features):
        if self.model is None:
            raise ValueError("Model not loaded.")

        return self.model.predict_proba(features)