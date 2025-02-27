import streamlit as st
import pandas as pd
import re

# Streamlit UI
st.title("📩 Email & Phone Extractor")
st.write("Upload a Notepad (`.txt`) file to extract emails and phone numbers.")

# File uploader
uploaded_file = st.file_uploader("Upload your Notepad file (.txt)", type=["txt"])

if uploaded_file is not None:
    # Read file content
    content = uploaded_file.read().decode("utf-8")

    # Use regex to find email addresses
    email_matches = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content)
    
    # Use regex to find phone numbers
    phone_matches = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
