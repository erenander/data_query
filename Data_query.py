import streamlit as st
import pandas as pd
import openai

# Function to load CSV file
def load_csv(file):
    df = pd.read_csv(file)
    return df

# Function to query OpenAI with a CSV and a user query using the new API format
def query_openai(df, user_query, openai_api_key):
    # Convert the dataframe to a string (limit size if necessary)
    df_str = df.to_csv(index=False)

    # Set up the OpenAI API key
    openai.api_key = openai_api_key

    # Create the prompt for OpenAI, combining the CSV data with the user's query
    prompt = f"Here is the data:\n{df_str}\n\nNow, based on this data, {user_query}"

    # Query OpenAI using the new Completions API format
    response = openai.Completion.create(
        model="gpt-3.5-turbo",  # You can use "gpt-4" as well if you have access
        prompt=prompt,
        max_tokens=500
    )

    # Return the response text
    return response['choices'][0]['text']

# Streamlit app interface
st.title("CSV Data Query App using OpenAI")

# File uploader widget for CSV
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

# Text input for user query
user_query = st.text_input("Enter your query about the data:")

# Get OpenAI API Key from Streamlit secrets
openai_api_key = st.secrets["openai_api_key"]

# When a file is uploaded and a query is provided
if uploaded_file is not None and user_query and openai_api_key.startswith("sk-"):
    # Load the CSV file into a dataframe
    df = load_csv(uploaded_file)
    
    # Display the dataframe
    st.write("### Uploaded DataFrame")
    st.write(df)
    
    # Query OpenAI and display the response
    st.write("### OpenAI's Response")
    response = query_openai(df, user_query, openai_api_key)
    st.write(response)
