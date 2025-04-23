import streamlit as st
import pandas as pd
import re

# Function to extract contacts
def extract_contacts(text):
    contacts = []
    # Split the text into potential contact blocks based on double newlines
    blocks = re.split(r'\n\s*\n', text)

    for block in blocks:
        email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', block)
        phone_matches = re.findall(r'(?:m|c|cell|mobile|direct|o|tel|telephone|office)[:\s\-|\\>;]?\s*(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})|(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})', block)

        cleaned_phones = [re.sub(r'[^0-9]', '', phone) for match in phone_matches for phone in match if phone]

        if email_match:
            email = email_match.group(0)
            phone1 = cleaned_phones[0] if len(cleaned_phones) > 0 else "Not Available"
            phone2 = cleaned_phones[1] if len(cleaned_phones) > 1 else "Not Available"
            contacts.append({"Email": email, "Phone 1": phone1, "Phone 2": phone2})

    return pd.DataFrame(contacts)

# Streamlit UI
st.title("📞 Email & Phone Extractor")

uploaded_file = st.file_uploader("Upload a Notepad (.txt) file", type="txt")

if uploaded_file:
    text = uploaded_file.read().decode("utf-8")
    df = extract_contacts(text)

    st.write("### Extracted Data:")
    st.dataframe(df)

    # Download button for CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", data=csv, file_name="Contacts_Details.csv", mime="text/csv")
