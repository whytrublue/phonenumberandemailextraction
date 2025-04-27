import streamlit as st
import pandas as pd
import re

def extract_contacts(text):
    # Patterns
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})'

    # Keywords for mobile
    mobile_keywords = ['c', 'm', 'mobile', 'cell', 'cellphone']

    # Extract all emails
    emails = re.findall(email_pattern, text)

    # Split text into blocks based on newline or separators
    blocks = re.split(r'\n|[\[\]\(\)\{\}\|]', text)

    results = []
    email_index = 0  # Track email position

    for block in blocks:
        block_lower = block.lower()
        phones = re.findall(phone_pattern, block)

        mobile = None
        office = None

        if phones:
            if any(kw in block_lower for kw in mobile_keywords):
                # Find which phone is Mobile based on proximity to keyword
                for kw in mobile_keywords:
                    match = re.search(rf'{kw}\s*[:=\-/>|]?\s*(\(?\d{{3}}\)?[-.\s]?\d{{3}}[-.\s]?\d{{4}})', block_lower)
                    if match:
                        mobile = match.group(1)
                        break
                # If two phones, assign the other one to office
                for phone in phones:
                    if phone != mobile:
                        office = phone
                        break
            else:
                if len(phones) == 2:
                    office = phones[0]
                    mobile = phones[1]
                elif len(phones) == 1:
                    office = phones[0]

            # Assign extracted email
            if email_index < len(emails):
                email = emails[email_index]
                email_index += 1

            results.append({
                'Email': email,
                'Mobile': mobile,
                'Office': office
            })
    return results

# Streamlit app
st.title("Extract Emails, Mobile, and Office Numbers 📄📞")

uploaded_file = st.file_uploader("Upload a Notepad (.txt) file", type=["txt"])

st.write("OR")

text_input = st.text_area("Paste your text here:")

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

    st.success("Extraction Completed Successfully ✅")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Extracted Data as CSV",
        data=csv,
        file_name="extracted_contacts.csv",
        mime='text/csv'
    )
