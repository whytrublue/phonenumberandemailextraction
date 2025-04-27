
import streamlit as st
import pandas as pd
import re

# --- App Header ---
st.set_page_config(page_title="📞 Email & Phone Extractor", layout="centered")
st.title("📞 Email & Phone Extractor")
st.markdown("Upload a Notepad (.txt) file and enter a custom separator (like READ MORE, -----, ###) to extract contacts.")

st.write("OR")

text_input = st.text_area("Paste your text here:")

# --- Separator Input ---
separator_input = st.text_input("✂️ Enter a custom separator between contacts (e.g., READ MORE, -----, ###)")

# --- File Upload ---
uploaded_file = st.file_uploader("📄 Upload a Notepad (.txt) file", type=["txt"])

# --- Function to Extract Contacts ---
def extract_contacts(text, separator):
    contacts = []

    # Use the provided separator or fallback to the dashed line separator if none is provided
    if separator.strip():
        escaped_sep = re.escape(separator.strip())
        blocks = re.split(rf'{escaped_sep}', text)
    else:
        blocks = re.split(r'(?:READ\s*MORE|[-=]{3,}|\n\s*\n){1,}', text, flags=re.IGNORECASE)

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # Split the block into lines to handle the name as the first line of each contact
        lines = block.splitlines()
        
        # The first line is treated as the Full Name
        name = lines[0].strip()

        # Extract email from the block
        email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', block)
        email = email_match.group(0) if email_match else ''

        # Extract phone numbers (up to 2 unique)
        phone_matches = re.findall(
            r'(?:m|c|cell|mobile|direct|o|tel|telephone|office)?[:\s\-|\\>;]?\s*(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})',
            block,
            flags=re.IGNORECASE
        )
        phone_matches = list(dict.fromkeys([p.strip() for p in phone_matches if p.strip()]))
        phone1 = phone_matches[0] if len(phone_matches) > 0 else ''
        phone2 = phone_matches[1] if len(phone_matches) > 1 else ''

        # Add the extracted information to contacts
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
    
    if st.button("Extract"):
    if uploaded_file is not None:
        text = uploaded_file.read().decode('utf-8')
    elif text_input:
        text = text_input
    else:
        st.error("Please upload a file or paste some text.")
        st.stop()

    extracted_data = extract_contacts(text)
    df = pd.DataFrame(extracted_data)

    csv = df.to_csv(index=False)
    st.download_button("📥 Download as CSV", csv, file_name="extracted_contacts.csv", mime='text/csv')

    # --- Copy to Clipboard (for Excel or Google Sheets) ---
    st.subheader("📄 Copy to Clipboard (Paste into Excel or Sheets)")
    tsv_text = df.to_csv(index=False, sep='\t')
    st.code(tsv_text, language='text')
else:
    st.warning("Please upload a Notepad file to extract contacts.")
