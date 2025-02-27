import streamlit as st
import pandas as pd
import re

def extract_contacts(text):
    # Extract emails
    email_matches = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)

    # Extract phone numbers
    phone_matches = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)

    # Create a list of dictionaries
    data_list = []
    for email in email_matches:
        data_list.append({"Email": email, "Phone": "Not Available"})
    
    for phone in phone_matches:
        for entry in data_list:
            if entry["Phone"] == "Not Available":
                entry["Phone"] = phone
                break

    return pd.DataFrame(data_list)

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
