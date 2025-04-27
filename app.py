import re
import pandas as pd
import streamlit as st

# Function to extract contact details
def extract_contact_details(text):
    # Regex patterns
    phone_pattern = r'(\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{4}|\d{3}[\s\-]?\d{3}[\s\-]?\d{4})'  # Capturing phone numbers
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'  # Capturing email addresses
    name_pattern = r'([A-Za-z]+(?: [A-Za-z]+)*)(?=\s*\n)'  # Capturing first and last names properly

    # Extract phone numbers, emails, and names
    phones = re.findall(phone_pattern, text)
    emails = re.findall(email_pattern, text)
    names = re.findall(name_pattern, text)

    # Prepare extracted data
    extracted_data = []
    
    # Checking if number of names, emails, and phones match
    if len(names) != len(emails):
        st.warning("Mismatch between the number of names and emails.")
    
    phone_idx = 0  # For iterating through phone numbers
    
    for i, name in enumerate(names):
        # For each name, get email and phone numbers
        email = emails[i] if i < len(emails) else None
        phone_list = []
        
        # Extract phone numbers related to the current entry
        while phone_idx < len(phones) and (phones[phone_idx] not in emails):  # Ensure not mixing emails with phones
            phone_list.append(phones[phone_idx])
            phone_idx += 1
        
        # Format phone numbers as a single string (in case there are multiple)
        phone_numbers = " | ".join(phone_list)

        extracted_data.append({
            'Name': name,
            'Email': email,
            'Phone Numbers': phone_numbers
        })
    
    return extracted_data

# Streamlit interface
def main():
    st.title("Contact Details Extractor")
    
    uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
    st.write("OR")
    text_input = st.text_area("Paste your text here:", height=200)

    if st.button("Extract"):
        if uploaded_file is not None:
            text = uploaded_file.read().decode('utf-8')
        elif text_input:
            text = text_input
        else:
            st.error("Please upload a file or paste some text.")
            st.stop()

        extracted_data = extract_contact_details(text)
        
        if not extracted_data:
            st.warning("No emails or phone numbers found.")
            st.stop()

        # Create DataFrame
        df = pd.DataFrame(extracted_data)
        
        # Display results
        st.subheader("Extracted Data")
        st.dataframe(df)
        
        # Format for copy-paste
        formatted_data = "\n".join(
            f"{row['Name']}\t{row['Email']}\t{row['Phone Numbers']}"
            for _, row in df.iterrows()
        )
        
        st.subheader("📋 Copy-Paste Format")
        st.code(formatted_data)
        
        # Download options
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download as CSV",
            data=csv,
            file_name="contacts.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
