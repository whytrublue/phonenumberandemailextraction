import streamlit as st
import pandas as pd
import re

def extract_contacts(text):
    # Patterns
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    phone_pattern = r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})'
    mobile_keywords = ['cell', 'c:', 'm:', 'mobile', 'cellphone']

    # Split into lines
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    results = []
    temp_record = {}

    for idx, line in enumerate(lines):
        # Find email
        email_match = re.search(email_pattern, line)
        phone_matches = re.findall(phone_pattern, line)

        if email_match:
            temp_record['Email'] = email_match.group(0)

            # Check if previous lines had mobile/office numbers
            j = idx - 1
            while j >= 0:
                previous_line = lines[j].lower()
                if any(keyword in previous_line for keyword in mobile_keywords):
                    phones = re.findall(phone_pattern, previous_line)
                    if phones:
                        temp_record['Mobile'] = phones[0]
                        if len(phones) > 1:
                            temp_record['Office'] = phones[1]
                    break
                elif '|' in previous_line:
                    phones = re.findall(phone_pattern, previous_line)
                    if phones:
                        temp_record['Office'] = phones[0]
                        if len(phones) > 1:
                            temp_record['Mobile'] = phones[1]
                    break
                j -= 1

            results.append(temp_record)
            temp_record = {}

        elif any(keyword in line.lower() for keyword in mobile_keywords):
            # If 'Cell:' or 'C:' appears and no email yet
            phones = re.findall(phone_pattern, line)
            if phones:
                temp_record['Mobile'] = phones[0]

        elif '|' in line:
            # If phones separated by |
            phones = re.findall(phone_pattern, line)
            if phones:
                temp_record['Office'] = phones[0]
                if len(phones) > 1:
                    temp_record['Mobile'] = phones[1]

    return results

# Streamlit app
st.title("📄📞 Extract Emails, Mobile, and Office Numbers (Handles All Formats)")

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

    # Display results
    st.subheader("Extracted Data Table")
    st.dataframe(df)

    # Text output for copying
    formatted_data = "\n".join(df.apply(lambda row: "\t".join(row.fillna('').astype(str)), axis=1))

    st.subheader("📋 Copy Extracted Data")
    st.code(formatted_data, language="text")

    # Download CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Extracted Data as CSV",
        data=csv,
        file_name="extracted_contacts.csv",
        mime='text/csv'
    )
