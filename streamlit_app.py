import streamlit as st
import os
import pandas as pd
from utils import get_response_with_retry

# Set your OpenAI API key as an environment variable
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Function to handle user request and generate a response
def handle_request(user_input):
    # Use the get_response_with_retry function from utils with the API key from the environment variable
    response = get_response_with_retry(user_input, api_key=OPENAI_API_KEY)
    return response

# Streamlit app interface
def main():
    # Streamlit app title
    st.title("Failure Post-Mortem Analysis")

    # Load CSV file with failure stories
    st.sidebar.header("Load Failure Stories")
    uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file is not None:
        stories_df = pd.read_csv(uploaded_file)
        selected_company = st.sidebar.selectbox("Select a failed company", stories_df['company'])
    else:
        st.sidebar.warning("Please upload a CSV file.")

    # Get user prompt using st.text_area
    user_prompt = st.text_area("Enter the prompt for analysis:")

    # Check if user has selected a company and entered a prompt
    if uploaded_file is not None and user_prompt:
        # Process user request and get failure reasons using handle_request function
        full_story = stories_df[stories_df['company'] == selected_company]['story'].values[0]
        user_input = f"{full_story}\n\nPrompt: {user_prompt}"
        failure_reasons = handle_request(user_input)

        # Display failure reasons using st.text
        st.subheader("Failure Reasons:")
        st.text(failure_reasons)

# Run the Streamlit app
if __name__ == "__main__":
    main()
