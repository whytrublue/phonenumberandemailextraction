# streamlit_app.py

import streamlit as st
import pandas as pd
import re

def extract_contacts(file_content):
    data_list = []

    # Use regex to find email addresses
    email_matches = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', file_content)
    
    # Use regex to find phone numbers
    phone_matches = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', file_content)

    # Create a list of dictionaries
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

st.write("Upload a Notepad file **or** paste your text below:")

# Upload option
uploaded_file = st.file_uploader("Upload Notepad (.txt) File", type=["txt"])

# Paste text option
pasted_text = st.text_area("Or paste your text here", height=200)

# Extract button
if st.button("Extract Contacts"):
    if uploaded_file:
        file_content = uploaded_file.read().decode("utf-8")
    elif pasted_text.strip():
        file_content = pasted_text
    else:
        st.warning("⚠️ Please upload a file or paste some text.")
        st.stop()

    # Extract contacts
    df = extract_contacts(file_content)

    if not df.empty:
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
    else:
        st.info("No contacts found in the provided content.")
