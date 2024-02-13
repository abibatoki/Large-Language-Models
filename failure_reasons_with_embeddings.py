import pandas as pd
from embeddings_utils import get_embedding
from vector_database import VectorDatabase

# Create an instance of VectorDatabase
vector_db = VectorDatabase()

# Load your failure reasons from the CSV file
failure_reasons_df = pd.read_csv(r'C:\Users\user\Downloads\updated_reasons.csv')  # Replace with the actual path to your CSV file

# Iterate through each row in the DataFrame
for index, row in failure_reasons_df.iterrows():
    document = row['reasons']  # Replace with the actual column name containing your failure reasons
    vector = get_embedding(document)  # Assuming you have a function to get embeddings
    vector_db.upsert(document, vector)

# Add a new column to the DataFrame containing the embeddings
failure_reasons_df['vector'] = failure_reasons_df['reasons'].apply(lambda x: vector_db.index.get(x, []))

# Save the DataFrame with the new column to a new CSV file
failure_reasons_df.to_csv(r'C:\Users\user\Desktop\failure_reasons_with_embeddings.csv', index=False)


