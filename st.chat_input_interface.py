import streamlit as st
import os
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

    # Get user story using st.chat_input
    user_story = st.text_area("Enter the failure post-mortem story:")

    # Check if user has entered a story
    if user_story:
        # Process user request and get failure reasons using handle_request function
        failure_reasons = handle_request(user_story)

        # Display failure reasons using st.text
        st.text(failure_reasons)

# Run the Streamlit app
if __name__ == "__main__":
    main()
