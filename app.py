import streamlit as st
import pandas as pd
import re

# Function to extract contacts
def extract_contacts(text):
    # Define regular expressions for phone numbers with special prefixes
    mobile_patterns = [
        r'(m[:\s\-|\\>;]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4})',  # m, m:, m followed by spaces or symbols
        r'(c[:\s\-|\\>;]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4})',  # c, c:, c followed by spaces or symbols
        r'(cell[:\s\-|\\>;]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4})',  # cell, cell phone, etc.
        r'(mobile[:\s\-|\\>;]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4})',  # mobile, mobile phone, mobile number
        r'(direct[:\s\-|\\>;]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4})'  # direct, direct phone, direct number
    ]

    office_patterns = [
        r'(o[:\s\-|\\>;]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4})',  # o, o:, o followed by symbols or spaces
        r'(tel[:\s\-|\\>;]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4})',  # tel, telephone, telephone number
        r'(telephone[:\s\-|\\>;]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4})',  # telephone
        r'(office[:\s\-|\\>;]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4})'  # office, office phone
    ]
    
    # Extract emails
    email_matches = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)

    # Combine all patterns and extract matching phone numbers
    mobile_matches = []
    office_matches = []

    for pattern in mobile_patterns:
        mobile_matches.extend(re.findall(pattern, text))
    
    for pattern in office_patterns:
        office_matches.extend(re.findall(pattern, text))

    # Clean and ensure there are no duplicates or unnecessary spaces
    mobile_matches = [re.sub(r'[^0-9]', '', phone) for phone in mobile_matches]
    office_matches = [re.sub(r'[^0-9]', '', phone) for phone in office_matches]

    # Create a list of dictionaries with email and phones
    data_list = []
    for email in email_matches:
        data = {"Email": email, "Phone 1": "Not Available", "Phone 2": "Not Available"}
        data_list.append(data)

    # Assign the first mobile number to Phone 1 and the second mobile number to Phone 2
    for idx, phone in enumerate(mobile_matches):
        if idx < len(data_list) and data_list[idx]["Phone 1"] == "Not Available":
            data_list[idx]["Phone 1"] = phone
        elif idx < len(data_list) and data_list[idx]["Phone 2"] == "Not Available":
            data_list[idx]["Phone 2"] = phone

    # Assign the first office number to Phone 1 and the second office number to Phone 2
    for idx, phone in enumerate(office_matches):
        if idx < len(data_list) and data_list[idx]["Phone 1"] == "Not Available":
            data_list[idx]["Phone 1"] = phone
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
