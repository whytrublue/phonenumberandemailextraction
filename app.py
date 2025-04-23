import streamlit as st
import pandas as pd
import re

def extract_contacts(text):
    # Extract emails
    email_matches = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)

    # Extract phone numbers with flexibility to handle different formats like "c:", spaces, etc.
    phone_matches = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    
    # Handle cases where phone numbers are listed with labels (like "c:", etc.)
    phone_matches = [phone.split(' ')[-1] for phone in phone_matches]  # Get the actual phone numbers
    
    # Create a list of dictionaries
    data_list = []
    for email in email_matches:
        data = {"Email": email, "Phone 1": "Not Available", "Phone 2": "Not Available"}
        data_list.append(data)

    for idx, phone in enumerate(phone_matches):
        # Assign the first phone number to "Phone 1"
        if idx < len(data_list) and data_list[idx]["Phone 1"] == "Not Available":
            data_list[idx]["Phone 1"] = phone
        # Assign the second phone number to "Phone 2"
        elif idx < len(data_list) and data_list[idx]["Phone 2"] == "Not Available":
            data_list[idx]["Phone 2"] = phone

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
