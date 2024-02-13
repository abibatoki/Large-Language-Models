import pandas as pd
import streamlit as st
from utils import get_response_with_retry, process_response
import os

# Retrieve your OpenAI API key from the environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Function to handle user request and generate a response
def handle_request(request):
    # Use your OpenAI API key
    api_key = OPENAI_API_KEY

    # Create the prompt using the user's story
    prompt = f"Extract the failure reason from this startup shutdown and summarize each reason in 5 words or less.\n\n{request}"

    # Use the OpenAI API to get the response
    response = get_response_with_retry(prompt, api_key=api_key)

    # Check if the response is not None before processing
    if response is not None:
        try:
            # Process the response using the utility function
            processed_response = process_response(response)
            return processed_response
        except Exception as e:
            st.error(f"Error processing API response: {e}")
            return "Failed to process the API response."
    else:
        return "Failed to get a response from the OpenAI API."

# Specify the path to your CSV file
csv_file_path = r'C:\Users\user\Downloads\stories.csv'  # Update with the actual path to your CSV file

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

# Add a new column called "reasons" to store the failure reasons
df['reasons'] = ""

# Process the first 10 rows and extract failure reasons
for index, row in df.head(10).iterrows():
    user_story = row["story"] + " " + row["quote"]
    failure_reasons = handle_request(user_story)

    # Add the list of failure reasons to the "reasons" column
    df.at[index, 'reasons'] = failure_reasons

# Save the updated DataFrame to a new CSV file
output_file_path = r'C:\Users\user\Downloads\updated_reasons.csv'  # Update with the desired output file path
df.head(10).to_csv(output_file_path, index=False)

# Display the updated DataFrame
st.dataframe(df.head(10))  # Display only the first 10 rows
st.success(f"Data saved to {r'C:\Users\user\Downloads\updated_reasons.xlsx'}")

