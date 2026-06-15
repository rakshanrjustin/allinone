import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

# Sample Dataset
df = pd.DataFrame({
    "salary": [25000, 30000, 28000, 80000, 85000, 90000],
    "spending": [2000, 2500, 2200, 10000, 12000, 11000]
})

print("Original Data:")
print(df)

# Data Scaling
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df)

print("\nScaled Data:")
print(df_scaled)

# ==========================
# ELBOW METHOD
# ==========================
wcss = []

for k in range(1, 7):
    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    kmeans.fit(df_scaled)
    wcss.append(kmeans.inertia_)

print("\nWCSS Values:")
print(wcss)

# Plot Elbow Curve
plt.figure(figsize=(6,4))
plt.plot(range(1, 7), wcss, marker="o")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("WCSS")
plt.title("Elbow Method")
plt.show()

# ==========================
# FINAL MODEL (K = 2)
# ==========================
kmeans = KMeans(
    n_clusters=2,
    random_state=42,
    n_init=10
)

kmeans.fit(df_scaled)

# Cluster Labels
df["cluster"] = kmeans.labels_

print("\nClustered Data:")
print(df)

# ==========================
# SILHOUETTE SCORE
# ==========================
score = silhouette_score(
    df_scaled,
    kmeans.labels_
)

print("\nSilhouette Score:")
print(score)

# ==========================
# VISUALIZATION
# ==========================
plt.figure(figsize=(6,4))
plt.scatter(
    df["salary"],
    df["spending"],
    c=df["cluster"]
)

plt.xlabel("Salary")
plt.ylabel("Spending")
plt.title("Customer Clusters")
plt.show()


