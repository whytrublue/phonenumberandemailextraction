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
    seen_lines = set()  # Set to track unique full lines (name, email, phone)

    i = 0
    while i < len(lines):
        line = lines[i].strip()  # Remove any leading/trailing whitespace
        if not line:  # Skip empty lines
            i += 1
            continue

        # Combine multiple lines into a single line (name, email, phone)
        full_line = line
        
        # Get the next lines for email and phone numbers (if available)
        if i + 1 < len(lines):
            full_line += " | " + lines[i + 1].strip()  # Add email
        
        if i + 2 < len(lines):
            full_line += " | " + lines[i + 2].strip()  # Add phone numbers

        # Skip if this full line has already been processed (duplicate)
        if full_line in seen_lines:
            i += 3  # Skip to the next contact
            continue
        
        # Add to the set of processed lines
        seen_lines.add(full_line)

        # Extract the name, email, and phone numbers
        name = lines[i].strip()

        # Safely extract email, ensuring re.search() didn't return None
        email_match = re.search(email_pattern, lines[i+1]) if i + 1 < len(lines) else None
        email = email_match.group(0) if email_match else ""

        # Safely extract phone numbers, ensuring re.findall() doesn't return an empty list
        phones = re.findall(phone_pattern, lines[i+2]) if i + 2 < len(lines) else []

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

# Streamlit app
st.title("Extract Emails, Mobile, and Office Numbers 📄📞")

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

    # Extract contact details
    extracted_data = extract_contact_details(text)
    
    # Display the results as a table
    df = pd.DataFrame(extracted_data)
    
    st.subheader("Extracted Data Table")
    st.dataframe(df)  # Display the dataframe in the UI

    # Format the extracted data for copy-pasting
    formatted_data = "\n".join(df.apply(lambda row: "\t".join(row.astype(str)), axis=1))

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
