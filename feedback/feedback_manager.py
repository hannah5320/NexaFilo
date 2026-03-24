from feedback.database import insert_feedback

def collect_feedback(cluster_id, avg_similarity, cluster_size, similarity_std):
    print(f"\nCluster {cluster_id}")
    print(f"Average Similarity: {avg_similarity:.4f}")
    print(f"Cluster Size: {cluster_size}")
    print(f"Similarity Std Dev: {similarity_std:.4f}")

    while True:
        response = input("Accept this cluster? (yes/no): ").strip().lower()

        if response in ["yes", "no"]:
            break

        print("Invalid input. Please type 'yes' or 'no'.")

    accepted = 1 if response == "yes" else 0

    insert_feedback(
        cluster_id,
        avg_similarity,
        cluster_size,
        similarity_std,
        accepted
    )