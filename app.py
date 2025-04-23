import streamlit as st
import pandas as pd
import re

# --- App Header ---
st.set_page_config(page_title="📞 Email & Phone Extractor", layout="centered")
st.title("📞 Email & Phone Extractor")
st.markdown("Upload a Notepad (.txt) file and enter a custom separator (like READ MORE, -----, ###) to extract contacts.")

# --- Separator Input ---
separator_input = st.text_input("✂️ Enter a custom separator between contacts (e.g., READ MORE, -----, ###)", value="READ MORE")

# --- File Upload ---
uploaded_file = st.file_uploader("📄 Upload a Notepad (.txt) file", type=["txt"])

# --- Function to Extract Contacts ---
def extract_contacts(text, separator):
    contacts = []

    # Default to fallback separators if nothing is provided
    if separator.strip():
        escaped_sep = re.escape(separator.strip())
        blocks = re.split(rf'{escaped_sep}', text)
    else:
        blocks = re.split(r'(?:READ\s*MORE|[-=]{3,}|\n\s*\n){1,}', text, flags=re.IGNORECASE)

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # Extract email
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

        # Attempt to extract name from first lines not containing emails/phones
        lines = block.splitlines()
        name = ''
        for line in lines:
            if email in line or re.search(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', line):
                continue
            line = line.strip()
            if line and not name:
                name = line

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

   # --- Copy to Clipboard Feature ---
copy_text = df.to_csv(index=False, sep='\t')  # Tab-separated for copy-paste

st.markdown("""
    <h4>📋 Copy Extracted Contacts</h4>
    <textarea id="copyBox" style="width:100%; height:200px; font-family: monospace; font-size: 14px;">{}</textarea>
    <button onclick="copyToClipboard()" style="margin-top: 10px;">📄 Copy to Clipboard</button>

    <script>
    function copyToClipboard() {{
        var copyText = document.getElementById("copyBox");
        copyText.select();
        document.execCommand("copy");
    }}
    </script>
""".format(copy_text), unsafe_allow_html=True)

