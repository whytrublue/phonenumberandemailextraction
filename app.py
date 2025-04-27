import streamlit as st
import pandas as pd
import re

# --- App Header ---
st.set_page_config(page_title="📞 Email & Phone Extractor", layout="centered")
st.title("📞 Email & Phone Extractor")
st.markdown("Upload a Notepad (.txt) file or paste text here, then enter a custom separator (like READ MORE, -----, ###) to extract contacts.")

# --- Custom CSS to style the components similarly ---
st.markdown("""
    <style>
        /* Style the custom separator to make it more compact */
        .stTextInput {
            width: 100% !important;  /* Make the separator take full width */
            margin-bottom: 10px !important;  /* Space between components */
        }
        /* Style the file uploader to look similar to the separator input */
        .stFileUploader div {
            width: 100% !important;  /* Use full width for the file upload */
            height: 40px !important;  /* Keep the height compact */
            padding: 5px !important;  /* Reduce padding */
            border-radius: 5px !important;  /* Rounded corners for consistency */
            border: 1px solid #ccc !important;  /* Border to make it look like a text input */
        }
        .stFileUploader input[type="file"] {
            height: 100% !important;  /* Make sure file input is full height */
            padding: 5px !important;  /* Padding inside the file input */
        }
        /* Optional: Adjust the text size of the file uploader */
        .stFileUploader label {
            font-size: 14px !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- Layout using Columns ---
col1, col2, col3 = st.columns([1, 3, 1])  # Create 3 columns with different widths

# --- Column 1: Custom Separator and File Upload Below ---
with col1:
    # Custom Separator Input
    separator_input = st.text_input("✂️ Enter a custom separator between contacts (e.g., READ MORE, -----, ###)")
    # File Upload
    uploaded_file = st.file_uploader("📄 Upload a Notepad (.txt) file", type=["txt"])

# --- Column 2: Text Area for User Input (with more space) ---
with col2:
    text_input = st.text_area("Or paste your text here:", height=300)

# --- Extract Button ---
if st.button("Extract"):
    if uploaded_file:
        text = uploaded_file.read().decode('utf-8')
    elif text_input:
        text = text_input
    else:
        st.error("Please upload a file or paste some text.")
        st.stop()

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
            email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA0-9]{2,}', block)
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

    # --- Process the Extraction ---
    results = extract_contacts(text, separator_input)
    df = pd.DataFrame(results)

    if df.empty:
        st.warning("No contacts found.")
    else:
        st.subheader("📋 Extracted Contacts")
        st.dataframe(df)

        # --- Download as CSV ---
        csv = df.to_csv(index=False)
        st.download_button("📥 Download as CSV", csv, file_name="extracted_contacts.csv", mime='text/csv')

        # --- Copy to Clipboard (for Excel or Google Sheets) ---
        st.subheader("📄 Copy to Clipboard (Paste into Excel or Sheets)")
        tsv_text = df.to_csv(index=False, sep='\t')
        st.code(tsv_text, language='text')
else:
    st.info("Upload a file or paste text, and enter a separator to extract contacts.")
