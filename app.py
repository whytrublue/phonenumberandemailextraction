import streamlit as st
import pandas as pd
import re

# --- App Header ---
st.set_page_config(page_title="📞 Email & Phone Extractor", layout="centered")
st.title("📞 Email & Phone Extractor")
st.markdown("Upload a Notepad (.txt) file and enter a custom separator (like `READ MORE`, `-----`, etc.) to extract contacts.")

# --- Separator Input ---
separator_input = st.text_input("✂️ Enter a custom separator between contacts (e.g., READ MORE, -----, ###)", value="READ MORE")

# --- File Upload ---
uploaded_file = st.file_uploader("📄 Upload a Notepad (.txt) file", type=["txt"])

# --- Function to Extract Contacts ---
def extract_contacts(text, separator):
    contacts = []
    escaped_sep = re.escape(separator.strip()) if separator.strip() else r'(?:READ\s*MORE|[-=]{3,}|\n\s*\n)'
    blocks = re.split(escaped_sep, text, flags=re.IGNORECASE)

    for block in blocks:
        if not block.strip():
            continue

        email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', block)
        email = email_match.group(0) if email_match else ''

        phone_matches = re.findall(
            r'(?:m|c|cell|mobile|direct|o|tel|telephone|office)?[:\s\-|\\>;]?\s*(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})',
            block,
            flags=re.IGNORECASE
        )
        phone_matches = list(dict.fromkeys(phone_matches))
        
        # Initialize phone numbers and labels
        phone1 = ''
        phone2 = ''
        phone1_type = ''
        phone2_type = ''

        if len(phone_matches) > 0:
            phone1 = phone_matches[0]
            if re.search(r'\b(cell|mobile|m|c)\b', block, re.IGNORECASE):
                phone1_type = 'Cell Phone'
            elif re.search(r'\b(office|tel|telephone|direct|o)\b', block, re.IGNORECASE):
                phone1_type = 'Office Phone'

        if len(phone_matches) > 1:
            phone2 = phone_matches[1]
            if re.search(r'\b(cell|mobile|m|c)\b', block, re.IGNORECASE):
                phone2_type = 'Cell Phone'
            elif re.search(r'\b(office|tel|telephone|direct|o)\b', block, re.IGNORECASE):
                phone2_type = 'Office Phone'

        lines = block.strip().splitlines()
        name = next((line.strip() for line in lines if line.strip() and '@' not in line and not re.search(r'\d{3}', line)), '')

        # Format phone numbers with type information
        formatted_phone1 = f"{phone1} ({phone1_type})" if phone1 and phone1_type else phone1
        formatted_phone2 = f"{phone2} ({phone2_type})" if phone2 and phone2_type else phone2

        contacts.append({
            'Full Name': name,
            'Email': email,
            'Phone 1': formatted_phone1,
            'Phone 2': formatted_phone2
        })

    return contacts

# --- Process Uploaded File ---
if uploaded_file:
    text = uploaded_file.read().decode('utf-8')
    results = extract_contacts(text, separator_input)
    df = pd.DataFrame(results)

    st.subheader("📋 Extracted Contacts")
    st.dataframe(df)

    csv = df.to_csv(index=False)
    st.download_button("📥 Download as CSV", csv, file_name="extracted_contacts.csv", mime='text/csv')
