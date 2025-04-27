import streamlit as st
import pandas as pd
import re

def extract_contacts(text):
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    mobile_keywords = ['cell', 'c:', 'mobile', 'm:']
    
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    
    results = []
    current = {}

    for line in lines:
        # Extract emails
        email_match = re.search(email_pattern, line)
        if email_match:
            if current:
                results.append(current)
                current = {}
            current['Email'] = email_match.group(0)

        # Extract phones
        phones = re.findall(phone_pattern, line)
        if phones:
            lower_line = line.lower()
            if '|' in line:
                if len(phones) >= 2:
                    current['Office'] = phones[0]
                    current['Mobile'] = phones[1]
            elif any(keyword in lower_line for keyword in mobile_keywords):
                current['Mobile'] = phones[0]
            else:
                if 'Office' not in current:
                    current['Office'] = phones[0]
                else:
                    current['Mobile'] = phones[0]

    if current:
        results.append(current)

    return results

# -------------- STREAMLIT FRONTEND --------------
st.set_page_config(page_title="Extract Emails and Phones", layout="centered")

st.title("📑 Email & Phone Extractor")

st.write("Paste your text below 👇 and get the extracted Email, Office, Mobile numbers in a table.")

uploaded_text = st.text_area("Paste your text here:", height=300)

if st.button("Extract Data"):
    if uploaded_text.strip() == "":
        st.warning("Please paste some text first.")
    else:
        data = extract_contacts(uploaded_text)
        df = pd.DataFrame(data)
        
        if not df.empty:
            st.success(f"✅ Extracted {len(df)} records successfully!")
            st.dataframe(df)

            # Download button
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name='extracted_contacts.csv',
                mime='text/csv',
            )
        else:
            st.error("❌ No contacts found in the text.")
