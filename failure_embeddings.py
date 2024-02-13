import json
import numpy as np
import pandas as pd
from embeddings_utils import get_embedding
from vector_database import VectorDatabase

# Load the vector database
db = VectorDatabase()
db.load(r’C:\Users\user\Desktop\vector_database.csv’)  # Change the path if necessary

# Create lists to store the documents and vectors
documents = db.documents()
vectors = db.vectors()

# Create a DataFrame
embedding_df = pd.DataFrame({"document": documents, "vector": vectors})

# Save the DataFrame to a CSV file
embedding_df.to_csv(r’C:\Users\user\Desktop\failure_embeddings.csv’)  # Change the path if necessary

