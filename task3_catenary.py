import numpy as np
import matplotlib.pyplot as plt

def detect_catenary(filtered_file, labels_file, output_prefix):
    # Load filtered point cloud (already ground-removed)
    filtered = np.load(filtered_file)

    # Load labels from DBSCAN
    labels = np.load(labels_file)

    # Remove noise
    core_points = filtered[labels != -1]
    core_labels = labels[labels != -1]

    # Compute spatial span for each cluster
    spans = {}
    for cluster_id in set(core_labels):
        cluster_points = core_points[core_labels == cluster_id]
        x_span = cluster_points[:, 0].max() - cluster_points[:, 0].min()
        y_span = cluster_points[:, 1].max() - cluster_points[:, 1].min()
        spans[cluster_id] = x_span + y_span

    # Get largest cluster (assumed to be catenary)
    largest_cluster_id = max(spans, key=spans.get)
    largest_points = core_points[core_labels == largest_cluster_id]

    min_x, max_x = largest_points[:, 0].min(), largest_points[:, 0].max()
    min_y, max_y = largest_points[:, 1].min(), largest_points[:, 1].max()

    print(f"=== {output_prefix.upper()} ===")
    print(f"Catenary cluster ID: {largest_cluster_id}")
    print(f"Bounding box (x): {min_x:.2f} – {max_x:.2f}")
    print(f"Bounding box (y): {min_y:.2f} – {max_y:.2f}")

    # Save plot
    plt.figure()
    plt.scatter(largest_points[:, 0], largest_points[:, 1], s=1, c='orange')
    plt.title(f"Catenary Cluster ({output_prefix})")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.tight_layout()
    plt.savefig(f"{output_prefix}_catenary.png")
    plt.close()


# === Run for both datasets ===

# Dataset 1
detect_catenary("dataset1_filtered.npy", "dataset1_labels.npy", "dataset1")

# Dataset 2
detect_catenary("dataset2_filtered.npy", "dataset2_labels.npy", "dataset2")
