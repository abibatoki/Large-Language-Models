import json
import numpy as np
import os
import pandas as pd
from embeddings_utils import cosine_similarity, get_embedding  # Assuming get_embedding handles different engines

class VectorDatabase:
    def __init__(self):
        self.index = {}

    def load(self, path):
        """
        Load the database from a file.
        """
        with open(path, "r") as file:
            # Each line is a json object with a document and a vector
            # Example: {"document": "content", "vector": [1, 2, 3]}
            for line in file:
                record = json.loads(line)
                self.index[record["document"]] = record["vector"]

    def save(self, path):
        """
        Save the database to a file.
        """
        with open(path, "w") as file:
            # Each line is a json object with a document and a vector
            for document, vector in self.index.items():
                record = {"document": document, "vector": vector}
                file.write(json.dumps(record) + "\n")

    def documents(self):
        """
        Return all the documents in the database.
        """
        return list(self.index.keys())

    def vectors(self):
        """
        Return all the vectors in the database.
        """
        return list(self.index.values())

    def upsert(self, document, vector):
        """
        Upsert (insert or update) a record into the database.
        """
        self.index[document] = vector

    def query(self, vector, top_k=5):
        """
        Query the database.
        """
        # Find the top top_k closest vectors
        # Assumes that the vectors are normalized
        results = [(doc, cosine_similarity(vec, vector))
                   for doc, vec in self.index.items()]
        # Sort the results by similarity
        results = sorted(results, key=lambda r: r[1], reverse=True)
        # Return the corresponding documents and their scores
        return results[:top_k]

    def delete(self, document):
        """
        Delete a record from the database.
        """
        del self.index[document]

if __name__ == "__main__":
    # Assuming 'updated_reasons' is your DataFrame with columns: company, title, product, story, quote, and reasons
    updated_reasons = pd.read_csv(r'C:\Users\user\Downloads\updated_reasons.csv')

    db = VectorDatabase()

    # Process each row and extract failure reasons
    for index, row in updated_reasons.iterrows():  # Fix the variable name from 'reasons_df' to 'updated_reasons'
        user_story = row["story"] + " " + row["quote"]
        failure_reasons = row["reasons"]

        # Create embeddings for the reasons (call get_embedding with the specified engine)
        embedding = get_embedding(failure_reasons, model='text-embedding-ada-002')  # Specify the engine

        # Upsert the embeddings into the database
        db.upsert(user_story, embedding)

    # Save the vector database
    db.save(r'C:\Users\user\Desktop\vector_database.csv1')  # Fix the quotation mark issue in the file path


