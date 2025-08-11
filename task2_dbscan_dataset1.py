import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import DBSCAN
from share import get_ground_level

# # Load dataset 1
pcd = np.load("dataset1.npy")

# Filter ground points
ground = get_ground_level(pcd)
filtered = pcd[pcd[:, 2] > ground + 0.5]

# Take only x and y for clustering
xy = filtered[:, :2]

# ---- Elbow Plot ----
neigh = NearestNeighbors(n_neighbors=5)
nbrs = neigh.fit(xy)
distances, _ = nbrs.kneighbors(xy)
distances = np.sort(distances[:, 4])
plt.figure()
plt.plot(distances)
plt.title("Elbow Method - Dataset 1")
plt.xlabel("Points sorted by distance to 5th neighbor")
plt.ylabel("5th Nearest Neighbor Distance")
plt.grid(True)
plt.tight_layout()
plt.savefig("dataset1_elbow_plot.png")
plt.close()

# ---- DBSCAN Clustering ----
eps = 2.5
db = DBSCAN(eps=eps, min_samples=5).fit(xy)
labels = db.labels_
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
print(f"Number of clusters (Dataset 1): {n_clusters}")

# ---- Plot Clusters ----
plt.figure()
plt.scatter(xy[:, 0], xy[:, 1], c=labels, cmap='tab10', s=1)
plt.title(f"DBSCAN: {n_clusters} clusters")
plt.xlabel("x axis")
plt.ylabel("y axis")
plt.tight_layout()
plt.savefig("dataset1_clusters.png")
plt.close()
np.save("dataset1_labels.npy", labels)
np.save("dataset1_filtered.npy", filtered)
