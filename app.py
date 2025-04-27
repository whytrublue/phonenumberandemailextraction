# streamlit_app.py

import streamlit as st
import pandas as pd
import re

# Function to extract contacts
def extract_contacts(file_content):
    data_list = []

    # Extract emails
    email_matches = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', file_content)

    # Split lines
    lines = file_content.splitlines()

    emails = []
    mobiles = []
    offices = []

    # Process line by line
    for line in lines:
        # Extract email
        email_in_line = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', line)
        if email_in_line:
            emails.extend(email_in_line)

        # Special case: look for office|c:mobile pattern
        if 'c:' in line.lower() or 'c ' in line.lower():
            parts = re.split(r'\||\-|\/', line)  # split using |, -, /
            for part in parts:
                if re.search(r'(?i)c[\s:=+>|]*\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', part.strip()):
                    mobile = re.search(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', part.strip()).group()
                else:
                    office = re.search(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', part.strip())
                    if office:
                        office = office.group()
                    else:
                        office = ''
            mobiles.append(mobile if 'mobile' in locals() else '')
            offices.append(office if 'office' in locals() else '')

        else:
            # Normal phone extraction if no "c:" found
            phones = re.findall(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', line)
            if phones:
                # Assume first phone as office
                if len(phones) == 2:
                    offices.append(phones[0])
                    mobiles.append(phones[1])
                elif len(phones) == 1:
                    offices.append(phones[0])
                    mobiles.append('')

    # Combine based on index
    max_len = max(len(emails), len(mobiles), len(offices))
    emails += [''] * (max_len - len(emails))
    mobiles += [''] * (max_len - len(mobiles))
    offices += [''] * (max_len - len(offices))

    data = {
        'Email': emails,
        'Mobile': mobiles,
        'Office': offices
    }

    return pd.DataFrame(data)

# Streamlit UI
st.title("📄 Smart Contact Extractor")

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
