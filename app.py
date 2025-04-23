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
        phone1 = phone_matches[0] if len(phone_matches) > 0 else ''
        phone2 = phone_matches[1] if len(phone_matches) > 1 else ''

        lines = block.strip().splitlines()
        name = next((line.strip() for line in lines if line.strip() and '@' not in line and not re.search(r'\d{3}', line)), '')

        contacts.append({
            'Full Name': name,
            'Email': email,
            'Phone 1': phone1,
            'Phone 2': phone2
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
    
        # Show TSV format for easy copy-paste into Excel/Sheets
    st.subheader("📋 Copy to Clipboard (Paste into Excel or Sheets)")
    tsv_text = df.to_csv(index=False, sep='\t')
    st.code(tsv_text, language='text')


