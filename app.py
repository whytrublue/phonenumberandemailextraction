import streamlit as st
import pandas as pd
import re

def extract_contacts(text):
    # Patterns
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    phone_pattern = r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})'

    # Keywords
    mobile_keywords = ['cell', 'c', 'm', 'mobile', 'cellphone']

    # Split text into lines
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    results = []
    i = 0

    while i < len(lines):
        line = lines[i]

        email = None
        mobile = None
        office = None

        # Find email
        if re.search(email_pattern, line, re.I):
            email_match = re.search(email_pattern, line)
            if email_match:
                email = email_match.group(0)

            # Look backwards to find mobile if missed
            j = i - 1
            while j >= 0:
                previous_line = lines[j].lower()
                if any(keyword in previous_line for keyword in mobile_keywords):
                    phone_match = re.search(phone_pattern, previous_line)
                    if phone_match:
                        mobile = phone_match.group(0)
                    break
                j -= 1

            results.append({
                'Email': email,
                'Mobile': mobile,
                'Office': office
            })

        # Find phones first (if phone appears before email)
        elif any(keyword in line.lower() for keyword in mobile_keywords) and re.search(phone_pattern, line):
            phone_match = re.search(phone_pattern, line)
            if phone_match:
                mobile = phone_match.group(0)

            # Look ahead for email
            j = i + 1
            while j < len(lines):
                next_line = lines[j]
                email_match = re.search(email_pattern, next_line)
                if email_match:
                    email = email_match.group(0)
                    results.append({
                        'Email': email,
                        'Mobile': mobile,
                        'Office': office
                    })
                    break
                j += 1

        # Also handle direct email/phone on the same line
        elif re.search(email_pattern, line) and re.search(phone_pattern, line):
            email_match = re.search(email_pattern, line)
            phone_match = re.search(phone_pattern, line)

            email = email_match.group(0)
            mobile = phone_match.group(0)

            results.append({
                'Email': email,
                'Mobile': mobile,
                'Office': office
            })

        i += 1

    return results

# Streamlit app
st.title("Extract Emails, Mobile, and Office Numbers 📄📞 (Updated Version)")

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
