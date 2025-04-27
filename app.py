import streamlit as st
import pandas as pd
import re

def extract_contacts(text):
    # Patterns
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})'

    # Keywords
    mobile_keywords = ['c', 'm', 'mobile', 'cell', 'cellphone']

    # Extract all emails
    emails = re.findall(email_pattern, text)

    # Split text into blocks based on newline
    blocks = re.split(r'\n', text)

    results = []
    email_index = 0  # Track email position

    for block in blocks:
        block_lower = block.lower()

        # Split further by symbols like |, -, :, =, /, <, > but keep them connected
        parts = re.split(r'[\|\-:=/<>]', block)
        parts = [p.strip() for p in parts if p.strip()]

        phones = []
        for part in parts:
            phones += re.findall(phone_pattern, part)

        mobile = None
        office = None

        if phones:
            # Priority 1: Look for mobile keyword and link number near it
            found_mobile = False
            for kw in mobile_keywords:
                mobile_search = re.search(rf'{kw}\s*[:=\-/>|<]?\s*(\(?\d{{3}}\)?[-.\s]?\d{{3}}[-.\s]?\d{{4}})', block_lower)
                if mobile_search:
                    mobile = mobile_search.group(1)
                    found_mobile = True
                    break

            # Priority 2: Assign remaining number(s)
            if found_mobile:
                for phone in phones:
                    if phone != mobile:
                        office = phone
                        break
            else:
                # No mobile keyword found
                if len(phones) >= 2:
                    office = phones[0]
                    mobile = phones[1]
                elif len(phones) == 1:
                    office = phones[0]

            # Assign extracted email
            if email_index < len(emails):
                email = emails[email_index]
                email_index += 1
            else:
                email = None

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

    # Display results as a table
    st.subheader("Extracted Data Table")
    st.dataframe(df)

    # Format the extracted data for copy-pasting
    formatted_data = "\n".join(df.apply(lambda row: "\t".join(row.astype(str)), axis=1))

    st.subheader("📋 Copy Extracted Data")
    st.code(formatted_data, language="text")

    # Option to download the extracted data as CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Extracted Data as CSV",
        data=csv,
        file_name="extracted_contacts.csv",
        mime='text/csv'
    )
