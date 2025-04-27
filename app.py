import streamlit as st
import pandas as pd
import re

def extract_contacts(text):
    # Patterns
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})'
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

        # Check if there are multiple phone numbers in the block
        if phones:
            # If there is a 'c:', assign the corresponding phone as mobile
            for phone in phones:
                if 'c:' in block_lower:
                    mobile = phone
                    phones.remove(phone)
                    break

            # If there are still phones left, assign the first one to office
            if phones:
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

    # Display results as a table
    st.subheader("Extracted Data Table")
    st.dataframe(df)  # This will show the data in a table format

    # Format the extracted data for copy-pasting, replacing None with empty string
    formatted_data = "\n".join(df.apply(lambda row: "\t".join([str(val) if val is not None else '' for val in row]), axis=1))

    # Display the formatted data with a copy option
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
