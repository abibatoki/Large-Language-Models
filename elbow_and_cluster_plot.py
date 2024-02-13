import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Load the embeddings from the CSV file
embedding_df = pd.read_csv(r'C:\Users\user\Desktop\failure_embeddings.csv')  # Replace with the actual path to your embeddings CSV file

# Sidebar for selecting the number of clusters (K)
k_value = st.sidebar.slider("Select the number of clusters (K)", 1, 25, 5)

# Get the embeddings
embeddings = embedding_df['vector'].apply(eval).tolist()

# Perform K-means clustering
kmeans = KMeans(n_clusters=k_value, random_state=42)
embedding_df['cluster'] = kmeans.fit_predict(embeddings)

# Display the Elbow Plot
st.subheader("Elbow Plot")
inertia_values = []
for i in range(1, 26):
    kmeans = KMeans(n_clusters=i, random_state=42)
    kmeans.fit(embeddings)
    inertia_values.append(kmeans.inertia_)

fig, ax = plt.subplots()
ax.plot(range(1, 26), inertia_values, marker='o')
ax.set_xlabel('Number of Clusters (K)')
ax.set_ylabel('Inertia')
st.pyplot(fig)

# Display the Cluster Plot
st.subheader("Cluster Plot")

# Reduce dimensionality with PCA for visualization
pca = PCA(n_components=2)
pca_result = pca.fit_transform(embeddings)
embedding_df['pca1'] = pca_result[:, 0]
embedding_df['pca2'] = pca_result[:, 1]

# Scatter plot
fig, ax = plt.subplots()
sns.scatterplot(x='pca1', y='pca2', hue='cluster', data=embedding_df, palette='viridis', ax=ax)
ax.set_xlabel('Principal Component 1')
ax.set_ylabel('Principal Component 2')
ax.set_title(f'K-means Clustering (K={k_value})')
st.pyplot(fig)

