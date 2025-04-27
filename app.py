import streamlit as st
import re
import pandas as pd

# Function to extract contact details
def extract_contact_details(text):
    # Regex patterns for email and phone numbers
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})'

    # Split the input into individual lines
    lines = text.split("\n")

    contacts = []
    i = 0
    while i < len(lines):
        name = lines[i].strip()  # Name is always on the current line
        email = re.search(email_pattern, lines[i+1])  # Email is usually on the next line
        if email:
            email = email.group(0)
        else:
            email = ""
        
        # Extract phone numbers from the next line (or the next line after)
        phones = re.findall(phone_pattern, lines[i+2])
        
        # Assign phone numbers
        office_phone = None
        mobile_phone = None
        if phones:
            if len(phones) == 1:
                office_phone = phones[0]
            elif len(phones) == 2:
                office_phone = phones[0]
                mobile_phone = phones[1]
        
        contacts.append({
            "Name": name,
            "Email": email,
            "Office Phone": office_phone,
            "Mobile Phone": mobile_phone
        })
        
        i += 3  # Move to the next contact entry (Name, Email, Phone block)

    return contacts


# Streamlit UI code
st.title("Contact Information Extractor 📄📞")

# File upload
uploaded_file = st.file_uploader("Upload a Notepad (.txt) file", type=["txt"])

# Text input area (alternative to upload)
text_input = st.text_area("Or paste your text here:")

if st.button("Extract Contacts"):
    if uploaded_file is not None:
        # If file is uploaded, read it
        text = uploaded_file.read().decode('utf-8')
    elif text_input:
        # If text is pasted
        text = text_input
    else:
        st.error("Please upload a file or paste some text.")
        st.stop()

    # Extract contact details from the text
    extracted_data = extract_contact_details(text)

    # Convert to DataFrame for better visualization
    df = pd.DataFrame(extracted_data)

    # Display the data in a table
    st.subheader("Extracted Contact Information")
    st.dataframe(df)

    # Format the extracted data for copy-pasting
    formatted_data = "\n".join(df.apply(lambda row: "\t".join(row.astype(str)), axis=1))

    # Display the formatted data
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
