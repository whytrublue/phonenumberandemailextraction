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

    # Initialize variables for Name and Job Title
    full_name = None
    job_title = None

    for block in blocks:
        block_lower = block.lower()

        # Check if the block is a heading (H1 to H6) for name and job title
        if block.startswith('#'):  # This indicates a heading (H1 to H6)
            heading_level = block.count('#')
            # Extracting Name and Job Title
            if heading_level == 1:  # H1 is assumed to be Name + Job Title
                name_job_title = block.strip('#').strip()  # Remove leading '#' and any extra spaces
                if not full_name:  # Assume first heading is Name
                    full_name = name_job_title
                else:  # Assume second heading is Job Title
                    job_title = name_job_title
        
        # Extract phone numbers
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
                'Full Name': full_name,
                'Job Title': job_title,
                'Email': email,
                'Mobile': mobile,
                'Office': office
            })

    return results

# Streamlit app
st.title("Extract Emails, Mobile, Office Numbers, Name, and Job Title 📄📞")

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

    # Format the extracted data for copy-pasting
    formatted_data = "\n".join(df.apply(lambda row: "\t".join(row.astype(str)), axis=1))

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
