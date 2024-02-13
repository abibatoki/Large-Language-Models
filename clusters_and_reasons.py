import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Load the failure reasons with embeddings
failure_reasons_df = pd.read_csv(r'C:\Users\user\Desktop\failure_reasons_with_embeddings.csv')  # Replace with the actual path to your CSV file

# Sidebar for selecting the number of clusters (K)
optimal_k =  5 # Replace with the optimal number of clusters you determined from the Elbow Plot
k_value = st.sidebar.slider("Select the number of clusters (K)", 1, 25, optimal_k)

# Extract the embeddings from the 'vector' column
embeddings = failure_reasons_df['vector'].apply(eval).tolist()

# Perform K-means clustering
kmeans = KMeans(n_clusters=k_value, random_state=42)
failure_reasons_df['cluster'] = kmeans.fit_predict(embeddings)

# Reduce dimensionality with PCA for visualization
pca = PCA(n_components=2)
pca_result = pca.fit_transform(embeddings)
failure_reasons_df['pca1'] = pca_result[:, 0]
failure_reasons_df['pca2'] = pca_result[:, 1]

# Display the Cluster Plot using Streamlit
st.subheader("Cluster Plot")

# Scatter plot
fig, ax = plt.subplots()
sns.scatterplot(x='pca1', y='pca2', hue='cluster', data=failure_reasons_df, palette='viridis', ax=ax)
ax.set_xlabel('Principal Component 1')
ax.set_ylabel('Principal Component 2')
ax.set_title(f'K-means Clustering (K=5)')
st.pyplot(fig)

# Display the reasons in each cluster
st.subheader("Reasons in Each Cluster")

for cluster_num in range(k_value):
    st.write(f"Cluster {cluster_num} Reasons:")
    cluster_reasons = failure_reasons_df.loc[failure_reasons_df['cluster'] == cluster_num, 'reasons'].tolist()
    st.write(cluster_reasons)
    st.write('\n')  # Add a separator between clusters

