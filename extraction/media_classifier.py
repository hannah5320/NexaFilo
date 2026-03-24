import os
import whisper
from sentence_transformers import util

MEDIA_EXTENSIONS = [
    ".mp4", ".mkv", ".mov",
    ".mp3", ".wav", ".m4a",
    ".mpeg", ".mpg"
]

AUDIO_EXTENSIONS = [
    ".mp3", ".wav", ".m4a",
    ".mpeg", ".mpg"
]

VIDEO_EXTENSIONS = [
    ".mp4", ".mkv", ".mov"
]

CATEGORIES = {
    "Movies": "movie cinema trailer film hollywood action drama",
    "Lectures": "lecture tutorial class teaching education training",
    "Music": "song music lofi mp3 melody instrumental audio",
    "Podcasts": "podcast discussion interview talkshow speaking",
    "Sports": "sports cricket football match highlights fifa nba",
    "Games": "gaming gameplay walkthrough stream esports",
}

CONFIDENCE_THRESHOLD = 0.25


class MediaClassifier:
    def __init__(self, embedder):
        self.embedder = embedder
        self.whisper_model = whisper.load_model("tiny")

        # Precompute category embeddings using SAME embedder
        self.category_embeddings = {
            cat: self.embedder.encode(desc)[0]
            for cat, desc in CATEGORIES.items()
        }

    def is_media(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        return ext in MEDIA_EXTENSIONS

    def transcribe(self, file_path):
        try:
            result = self.whisper_model.transcribe(file_path, fp16=False)
            return result["text"]
        except Exception as e:
            print(f"[Whisper Error] {file_path}: {e}")
            return ""

    def classify(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()

        transcript = self.transcribe(file_path)

        text_to_analyze = os.path.basename(file_path) + " " + transcript
        file_embedding = self.embedder.encode(text_to_analyze)[0]

        best_category = "Unsorted"
        best_score = -1

        for category, cat_emb in self.category_embeddings.items():
            score = util.cos_sim(file_embedding, cat_emb).item()

            if score > best_score:
                best_score = score
                best_category = category

        # If similarity strong enough → trust semantic result
        if best_score >= CONFIDENCE_THRESHOLD:
            return best_category

        # ---------- Deterministic fallback ----------
        if ext in AUDIO_EXTENSIONS:
            return "Music"

        if ext in VIDEO_EXTENSIONS:
            return "Movies"

        return "Unsorted"