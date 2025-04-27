# streamlit_app.py

import streamlit as st
import pandas as pd
import re
import io

def extract_contacts(file_content):
    data_list = []

    # Use regex to find email addresses
    email_matches = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', file_content)
    
    # Use regex to find phone numbers
    phone_matches = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', file_content)

    # Create a unique set of email and phone matches
    for email in email_matches:
        data_list.append({
            'Email': email,
            'Phone': 'Not Available'
        })

    for phone in phone_matches:
        existing_entry = next((entry for entry in data_list if entry['Phone'] == 'Not Available'), None)
        if existing_entry:
            existing_entry['Phone'] = phone

    return pd.DataFrame(data_list)

# Streamlit UI
st.title("📄 Contact Details Extractor")

uploaded_file = st.file_uploader("Upload a Notepad (.txt) file", type=["txt"])

if uploaded_file:
    # Read file content
    file_content = uploaded_file.read().decode("utf-8")

    # Extract data
    df = extract_contacts(file_content)

    # Show the extracted DataFrame
    st.subheader("Extracted Contacts:")
    st.dataframe(df)

    # Prepare CSV for download
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Contacts CSV",
        data=csv,
        file_name="Contacts_Details.csv",
        mime="text/csv"
    )
