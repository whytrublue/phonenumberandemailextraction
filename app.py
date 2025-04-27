import streamlit as st
import pandas as pd
import re

# Function to extract emails and phone numbers
def extract_contacts(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'

    mobile_keywords = ['c', 'm', 'mobile', 'cell', 'cellphone']
    office_keywords = ['office', 'tel', 'telephone', 'direct', 'd', 'o', 't']

    emails = re.findall(email_pattern, text)
    phone_blocks = re.split(r'\n|[\[\]\(\)\{\}\|]', text)  # split on new lines and separators like |, [], {}, ()
    results = []

    for block in phone_blocks:
        block_lower = block.lower()

        # Find all phone numbers in the block
        phones = re.findall(phone_pattern, block)

        # Assign default values
        mobile = None
        office = None

        if phones:
            for phone in phones:
                # Check for mobile keyword near the phone
                if any(re.search(r'\b' + kw + r'\b\s*[:=\-/>|]?\s*' + re.escape(phone), block_lower) for kw in mobile_keywords):
                    mobile = phone
                # Check for office keyword near the phone
                elif any(re.search(r'\b' + kw + r'\b\s*[:=\-/>|]?\s*' + re.escape(phone), block_lower) for kw in office_keywords):
                    office = phone

            # If no clear mobile/office keyword, and 2 phones present
            if not mobile and not office and len(phones) == 2:
                mobile = phones[1]  # assume second number is mobile if | separator is used
                office = phones[0]  # first number is office

            # If only one phone and no keyword, assume it's office
            if not mobile and not office and len(phones) == 1:
                office = phones[0]

        # Assign extracted details
        result = {
            'Email': None,  # we'll fill email later
            'Mobile': mobile,
            'Office': office
        }
        results.append(result)

    # Now assign emails one by one
    for i, email in enumerate(emails):
        if i < len(results):
            results[i]['Email'] = email
        else:
            # more emails than phone entries
            results.append({'Email': email, 'Mobile': None, 'Office': None})

    return results

# Streamlit UI
st.title("Extract Emails, Mobile, and Office Numbers 📄📞")

# File upload option
uploaded_file = st.file_uploader("Upload a Notepad (.txt) file", type=["txt"])

# Textbox option
st.write("OR")
text_input = st.text_area("Paste text here")

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

    st.success("Extraction Complete!")
    st.dataframe(df)

    # Download option
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Extracted Data as CSV",
        data=csv,
        file_name='extracted_contacts.csv',
        mime='text/csv',
    )
