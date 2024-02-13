import pandas as pd
import streamlit as st
import numpy as np
from sklearn.cluster import KMeans

# Load the failure reasons with embeddings
failure_reasons_df = pd.read_csv(r'C:\Users\user\Desktop\failure_reasons_with_embeddings.csv')  # Replace with the actual path to your CSV file

# Extract the embeddings from the 'vector' column
failure_reasons_df['vector'] = failure_reasons_df['vector'].apply(eval)  # Convert string to list

# Sidebar for selecting the number of clusters (K)
k_value = st.sidebar.slider("Select the number of clusters (K)", 1, 25, 5)

# Perform K-means clustering
kmeans = KMeans(n_clusters=k_value, random_state=42)
failure_reasons_df['cluster'] = kmeans.fit_predict(failure_reasons_df['vector'].tolist())

# Handle cases where 'vector' column contains empty lists
def safe_mean(x):
    x = [v for v in x if v]  # Remove empty lists
    return np.mean(x, axis=0) if x else np.nan

# Statistical summary for each cluster
cluster_summaries = []

for cluster_num in range(k_value):
    cluster_data = failure_reasons_df[failure_reasons_df['cluster'] == cluster_num]['vector']
    cluster_summary = pd.Series({
        'min': np.min(cluster_data),
        'median': np.median(cluster_data, axis=0),
        'mean': safe_mean(cluster_data),
        'max': np.max(cluster_data)
    })
    cluster_summaries.append(cluster_summary)

    # Display the statistical summary for each cluster
    st.title(f'Statistical Summary of Embeddings for Cluster {cluster_num}')
    st.dataframe(cluster_summary)

# Optionally, you can store the cluster summaries in a single DataFrame
all_cluster_summaries = pd.concat(cluster_summaries, axis=1).transpose()

# Display the overall statistical summary for all clusters
st.title('Overall Statistical Summary of Embeddings for All Clusters')
st.dataframe(all_cluster_summaries)


