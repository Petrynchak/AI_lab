import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import pairwise_distances_argmin_min
import matplotlib.pyplot as plt

# Згенеруємо тестову послідовність з N значень, що є парами дійсних чисел на одиничному квадраті.
N = 1000
data = np.random.rand(N, 2)

# Реалізуємо допоміжну функцію для обчислення міри віддалі (використаємо евклідову відстань).
def distance_measure(a, b):
    distance = np.linalg.norm(a - b)
    return distance

# Реалізуємо допоміжну функцію для виконання алгоритму кластеризації за методом К-середніх.
def k_means_clustering(data, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(data)
    centroids = kmeans.cluster_centers_
    labels = kmeans.labels_
    return centroids, labels

# Реалізуємо допоміжну функцію для виконання алгоритму кластеризації за ієрархічним методом.
def hierarchical_clustering(data, n_clusters):
    hierarchical = AgglomerativeClustering(n_clusters=n_clusters)
    hierarchical.fit(data)
    labels = hierarchical.labels_
    return labels

# Безпосередньо реалізуємо кластеризацію даних двома методами та порівнюємо результати кластеризації.
k = 5  # Кількість кластерів
centroids_kmeans, labels_kmeans = k_means_clustering(data, k)
labels_hierarchical = hierarchical_clustering(data, k)

# Визначаємо якість кластеризації за середньо-зваженим розміром кластерів.
def clustering_quality(data, labels, centroids):
    n_clusters = len(centroids)
    cluster_sizes = np.bincount(labels)
    average_cluster_sizes = np.zeros(n_clusters)
    for i in range(n_clusters):
        cluster_points = data[labels == i]
        centroid = centroids[i]
        average_cluster_sizes[i] = np.mean([distance_measure(point, centroid) for point in cluster_points])
    weighted_average_cluster_size = np.dot(cluster_sizes, average_cluster_sizes) / len(data)
    return weighted_average_cluster_size

quality_kmeans = clustering_quality(data, labels_kmeans, centroids_kmeans)
quality_hierarchical = clustering_quality(data, labels_hierarchical, centroids_kmeans)

print("Кластеризація за методом K-середніх:", quality_kmeans)
print("Кластеризація за ієрархічним методом:", quality_hierarchical)

# Порівняємо кількість кластерів та якість кластеризації
print("Кількість кластерів - K-середніх:", len(np.unique(labels_kmeans)))
print("Кількість кластерів - Ієрархічна:", len(np.unique(labels_hierarchical)))

# Оцінимо середньо-зважений розмір кластерів для кожного методу
def average_cluster_size(data, labels, centroids):
    n_clusters = len(centroids)
    cluster_sizes = np.bincount(labels)
    average_cluster_sizes = np.zeros(n_clusters)
    for i in range(n_clusters):
        cluster_points = data[labels == i]
        centroid = centroids[i]
        average_cluster_sizes[i] = np.mean([distance_measure(point, centroid) for point in cluster_points])
    return np.mean(average_cluster_sizes)

average_cluster_size_kmeans = average_cluster_size(data, labels_kmeans, centroids_kmeans)
average_cluster_size_hierarchical = average_cluster_size(data, labels_hierarchical, centroids_kmeans)

print("Середній розмір кластера - K-середніх:", average_cluster_size_kmeans)
print("Середній розмір кластера - Ієрархічна:", average_cluster_size_hierarchical)

# Візуалізація результатів кластеризації
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.scatter(data[:, 0], data[:, 1], c=labels_kmeans, cmap='viridis', s=8)
plt.scatter(centroids_kmeans[:, 0], centroids_kmeans[:, 1], c='red', marker='x', s=100)
plt.title('Кластеризація за методом K-середніх')

plt.subplot(1, 2, 2)
plt.scatter(data[:, 0], data[:, 1], c=labels_hierarchical, cmap='viridis', s=8)
plt.title('Ієрархічна кластеризація')

plt.show()
