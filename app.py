import streamlit as st
import pandas as pd
import re

# Function to extract contacts from a block of text
def extract_contacts(text, separator):
    contacts = []

    # Escape special characters in custom separator
    escaped_sep = re.escape(separator.strip())

    # Fallback pattern if separator not provided
    if escaped_sep:
        blocks = re.split(escaped_sep, text)
    else:
        # Default fallback: READ MORE, dashed lines, or double newlines
        blocks = re.split(r'(?:READ\s*MORE|[-=]{3,}|\n\s*\n)', text, flags=re.IGNORECASE)

    for block in blocks:
        if not block.strip():
            continue

        # Extract email
        email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', block)
        email = email_match.group(0) if email_match else ''

        # Extract phone numbers
        phone_matches = re.findall(
            r'(?:m|c|cell|mobile|direct|o|tel|telephone|office)?[:\s\-|\\>;]?\s*(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})',
            block,
            flags=re.IGNORECASE
        )
        phone_matches = list(dict.fromkeys(phone_matches))  # remove duplicates

        phone1 = phone_matches[0] if len(phone_matches) > 0 else ''
        phone2 = phone_matches[1] if len(phone_matches) > 1 else ''

        # Extract name (first line without email or number)
        lines = block.strip().splitlines()
        name = next((line.strip() for line in lines if line.strip() and '@' not in line and not re.search(r'\d{3}', line)), '')

        contacts.append({
            'Full Name': name,
            'Email': email,
            'Phone 1': phone1,
            'Phone 2': phone2
        })

    return contacts

# Streamlit UI
st.title("Custom Contact Extractor")
uploaded_file = st.file_uploader("Upload a Notepad (.txt) file", type=["txt"])

separator_input = st.text_input("Enter custom separator (e.g., READ MORE, ----, etc.)")

if uploaded_file is not None:
    text = uploaded_file.read().decode('utf-8')
    extracted_contacts = extract_contacts(text, separator_input)
    df = pd.DataFrame(extracted_contacts)
    st.dataframe(df)
    csv = df.to_csv(index=False)
    st.download_button("Download CSV", csv, file_name="extracted_contacts.csv")
