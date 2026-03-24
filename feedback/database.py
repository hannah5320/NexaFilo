import sqlite3
from config import DATABASE_PATH

def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cluster_id INTEGER,
            avg_similarity REAL,
            cluster_size INTEGER,
            similarity_std REAL,
            accepted INTEGER
        )
    """)

    conn.commit()
    conn.close()


def insert_feedback(cluster_id, avg_similarity, cluster_size, similarity_std, accepted):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO feedback 
        (cluster_id, avg_similarity, cluster_size, similarity_std, accepted)
        VALUES (?, ?, ?, ?, ?)
    """, (cluster_id, avg_similarity, cluster_size, similarity_std, accepted))

    conn.commit()
    conn.close()


def fetch_feedback():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT avg_similarity, cluster_size, similarity_std, accepted 
        FROM feedback
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows
