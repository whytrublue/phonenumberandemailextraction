# streamlit_app.py

import streamlit as st
import pandas as pd
import re

# Function to extract contacts
def extract_contacts(file_content):
    data_list = []

    # Extract emails
    email_matches = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', file_content)

    # Extract labeled phone numbers
    phone_pattern = re.compile(r'(?i)(C|M|Mobile|Cell|Cellphone)[\s:=+>|]*\s*(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})')
    office_phone_pattern = re.compile(r'(?i)(Office|Telephone|Phone)[\s:=+>|]*\s*(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})')

    # Find matches
    mobile_matches = phone_pattern.findall(file_content)
    office_matches = office_phone_pattern.findall(file_content)

    # Find all phone numbers (whether labeled or not)
    all_phones = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', file_content)

    used_numbers = set()

    # Create initial list from emails
    for email in email_matches:
        data_list.append({
            'Email': email,
            'Mobile': '',
            'Office': ''
        })

    # Assign mobile numbers first
    for label, mobile in mobile_matches:
        for entry in data_list:
            if not entry['Mobile']:
                entry['Mobile'] = mobile
                used_numbers.add(mobile)
                break

    # Assign office numbers
    for label, office in office_matches:
        for entry in data_list:
            if not entry['Office']:
                entry['Office'] = office
                used_numbers.add(office)
                break

    # For remaining phone numbers that were not labeled
    for phone in all_phones:
        if phone not in used_numbers:
            for entry in data_list:
                if not entry['Mobile']:
                    entry['Mobile'] = phone
                    used_numbers.add(phone)
                    break
                elif not entry['Office']:
                    entry['Office'] = phone
                    used_numbers.add(phone)
                    break

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
