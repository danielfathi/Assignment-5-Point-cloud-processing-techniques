import numpy as np
import matplotlib.pyplot as plt

def get_ground_level(pcd, dataset_name):
    z = pcd[:, 2]  

    # histogram
    counts, bins = np.histogram(z, bins=100)
    max_index = np.argmax(counts)
    ground_level = (bins[max_index] + bins[max_index + 1]) / 2

  
    plt.figure()
    plt.hist(z, bins=100, color='gray')
    plt.axvline(ground_level, color='red', linestyle='--', label=f"Ground ≈ {ground_level:.2f}")
    plt.title(f"{dataset_name} - Ground Level Estimation")
    plt.xlabel("Z Height")
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{dataset_name.lower().replace(' ', '_')}_ground_histogram.png")
    plt.close()

    return ground_level


pcd1 = np.load('dataset1.npy')
pcd2 = np.load('dataset2.npy')

# ground level
ground1 = get_ground_level(pcd1, "Dataset 1")
ground2 = get_ground_level(pcd2, "Dataset 2")


print(f"Dataset 1 Ground Level: {ground1:.2f}")
print(f"Dataset 2 Ground Level: {ground2:.2f}")
